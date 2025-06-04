import os
import pandas as pd
from flask import Flask, render_template, request, send_from_directory, redirect
from werkzeug.utils import secure_filename
import subprocess
import sys
import time
from src.taxonomy_service import unspsc_map
from src.taxonomy_service import unspsc_dropdown_map
import psycopg2
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def prettify_column(col):
    return ' '.join(word.capitalize() for word in col.split('_'))

UPLOAD_FOLDER = 'uploads'
RESULTS_FOLDER = 'results'
ALLOWED_EXTENSIONS = {'csv'}

app = Flask(__name__)

# Database configuration
def get_db_connection():
    return psycopg2.connect(
        host=os.getenv('DB_HOST'),
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASSWORD'),
        database=os.getenv('DB_NAME')
    )

def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Create categorized table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS categorized (
            invoice_id INTEGER PRIMARY KEY,
            description TEXT,
            supplier TEXT,
            commodity_code VARCHAR(8),
            commodity_title TEXT,
            confidence FLOAT,
            source VARCHAR(50)
        )
    ''')
    
    # Create manual_review table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS manual_review (
            invoice_id INTEGER PRIMARY KEY,
            description TEXT,
            supplier TEXT,
            commodity_code VARCHAR(8),
            commodity_title TEXT,
            confidence FLOAT,
            source VARCHAR(50)
        )
    ''')
    
    conn.commit()
    cursor.close()
    conn.close()

# Initialize database on startup
init_db()

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['RESULTS_FOLDER'] = RESULTS_FOLDER

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(RESULTS_FOLDER, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Helper functions for database operations
def get_manual_review_data():
    conn = get_db_connection()
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    cursor.execute('SELECT * FROM manual_review')
    data = cursor.fetchall()
    cursor.close()
    conn.close()
    return data

def get_categorized_data():
    conn = get_db_connection()
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    cursor.execute('SELECT * FROM categorized')
    data = cursor.fetchall()
    cursor.close()
    conn.close()
    return data

def save_to_categorized(row_data):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO categorized 
        (invoice_id, description, supplier, commodity_code, commodity_title, confidence, source)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        ON CONFLICT (invoice_id) DO UPDATE SET
        commodity_code = EXCLUDED.commodity_code,
        commodity_title = EXCLUDED.commodity_title,
        confidence = EXCLUDED.confidence,
        source = EXCLUDED.source
    ''', (
        row_data['invoice_id'],
        row_data['description'],
        row_data['supplier'],
        row_data['commodity_code'],
        row_data['commodity_title'],
        row_data['confidence'],
        row_data.get('source', 'Manual')
    ))
    conn.commit()
    cursor.close()
    conn.close()

def remove_from_manual_review(invoice_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM manual_review WHERE invoice_id = %s', (invoice_id,))
    conn.commit()
    cursor.close()
    conn.close()

@app.route("/manual_review", methods=["GET", "POST"])
def manual_review():
    # Get data from database
    data = get_manual_review_data()
    
    if not data:
        return render_template(
            "manual_review.html",
            data=[],
            unspsc_dropdown_map=unspsc_dropdown_map,
            error="No invoices to review!"
        )

    if request.method == "POST":
        invoice_id = int(request.form.get("invoice_id"))
        corrected_code = request.form.get("corrected_code")

        # Get the row from manual_review
        conn = get_db_connection()
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        cursor.execute('SELECT * FROM manual_review WHERE invoice_id = %s', (invoice_id,))
        row = cursor.fetchone()
        cursor.close()
        conn.close()

        if row:
            # Update the row with corrected code
            row['commodity_code'] = corrected_code
            row['commodity_title'] = unspsc_dropdown_map[corrected_code]
            row['confidence'] = 1.0
            row['source'] = 'Manual'

            # Save to categorized and remove from manual_review
            save_to_categorized(row)
            remove_from_manual_review(invoice_id)

            return render_template(
                "manual_review.html",
                data=get_manual_review_data(),
                unspsc_dropdown_map=unspsc_dropdown_map,
                success=True,
                download_link="/download_categorized"
            )

    return render_template(
        "manual_review.html",
        data=data,
        unspsc_dropdown_map=unspsc_dropdown_map
    )

@app.route("/download_categorized")
def download_categorized():
    # Get data from database
    data = get_categorized_data()
    df = pd.DataFrame(data)
    
    # Format the data
    df.columns = [prettify_column(c) for c in df.columns]
    if 'Confidence Rounded' in df.columns:
        df = df.drop(columns=['Confidence Rounded'])
    df = df.rename(columns={
        "Commodity Title": "UNSPSC Category Name",
        "Commodity Code": "UNSPSC Category ID"
    })
    
    # Save to temporary CSV and send
    temp_path = "data/temp_categorized.csv"
    df.to_csv(temp_path, index=False)
    try:
        return send_from_directory(directory="data", path="temp_categorized.csv", as_attachment=True)
    finally:
        try:
            os.remove(temp_path)
        except:
            pass

@app.route("/download_manual")
def download_manual():
    # Get data from database
    data = get_manual_review_data()
    df = pd.DataFrame(data)
    
    # Save to temporary CSV and send
    temp_path = "data/temp_manual.csv"
    df.to_csv(temp_path, index=False)
    try:
        return send_from_directory(directory="data", path="temp_manual.csv", as_attachment=True)
    finally:
        try:
            os.remove(temp_path)
        except:
            pass

@app.route("/", methods=["GET", "POST"])
def index():
    result_table = None
    chart_data = []
    pie_chart_data = []
    confidence_pie_data = []
    amount_chart_data = []
    error = None
    elapsed = None
    uploaded_filename = None

    if request.method == "POST":
        invoice_file = request.files.get("invoice_file")

        if not invoice_file or not allowed_file(invoice_file.filename):
            error = "Please upload a valid invoice CSV file."
            return render_template(
                "index.html",
                error=error,
                elapsed=elapsed,
                chart_data=chart_data,
                pie_chart_data=pie_chart_data,
                result_table=result_table,
                confidence_pie_data=confidence_pie_data,
                amount_chart_data=amount_chart_data,
                uploaded_filename=uploaded_filename
            )

        uploaded_filename = secure_filename(invoice_file.filename)
        invoice_path = os.path.join(app.config['UPLOAD_FOLDER'], uploaded_filename)
        invoice_file.save(invoice_path)

        # Move uploaded file to data/sample_invoices.csv
        os.replace(invoice_path, "data/sample_invoices.csv")

        # Time logging start
        start_time = time.time()

        # Run the pipeline
        result = subprocess.run(
            [sys.executable, "-m", "src.pipeline"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )

        # Time logging end
        elapsed = time.time() - start_time
        print(f"Model pipeline execution time: {elapsed:.2f} seconds")

        if result.returncode != 0:
            error = "Error running categorization pipeline: " + result.stderr
            return render_template(
                "index.html",
                error=error,
                elapsed=elapsed,
                chart_data=chart_data,
                pie_chart_data=pie_chart_data,
                result_table=result_table,
                amount_chart_data=amount_chart_data,
                confidence_pie_data=confidence_pie_data,
                uploaded_filename=uploaded_filename
            )

        # Get data from database for display
        data = get_categorized_data()
        result_df = pd.DataFrame(data)

        if not result_df.empty:
            # Create charts and process data as before
            confidence_col = 'confidence'
            source_col = 'source'

            if confidence_col in result_df.columns:
                temp_df = result_df.copy()
                temp_df['Confidence Rounded'] = temp_df[confidence_col].round(4)
                
                # Your existing chart creation code here
                # ... (keep all your chart creation code)

            result_table = result_df.to_dict(orient='records')

    return render_template(
        "index.html",
        error=error,
        elapsed=elapsed,
        chart_data=chart_data,
        pie_chart_data=pie_chart_data,
        result_table=result_table,
        confidence_pie_data=confidence_pie_data,
        amount_chart_data=amount_chart_data,
        uploaded_filename=uploaded_filename
    )

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)