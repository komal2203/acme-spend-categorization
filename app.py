import os
import sys
import time
import gc
import psutil
import logging
import subprocess
from flask import Flask, request, render_template, jsonify
from werkzeug.utils import secure_filename
import pandas as pd
import json

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__)

# Configure upload folder
UPLOAD_FOLDER = 'data'
ALLOWED_EXTENSIONS = {'csv'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Ensure upload folder exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def log_memory_usage():
    process = psutil.Process(os.getpid())
    memory_info = process.memory_info()
    logger.info(f"Memory usage: {memory_info.rss / 1024 / 1024:.2f} MB")

def get_categorized_data():
    try:
        # Read the processed data from your ML pipeline output
        # This should match your pipeline's output format
        with open('data/processed_results.json', 'r') as f:
            return json.load(f)
    except Exception as e:
        logger.error(f"Error reading categorized data: {str(e)}")
        return []

def calculate_chart_data(df):
    try:
        # Calculate chart data based on your requirements
        chart_data = []
        pie_chart_data = []
        confidence_pie_data = []
        amount_chart_data = []
        
        # Example calculations (modify based on your needs):
        if not df.empty:
            # Category distribution
            category_counts = df['category'].value_counts().to_dict()
            pie_chart_data = [{'name': k, 'value': v} for k, v in category_counts.items()]
            
            # Confidence distribution
            confidence_counts = df['confidence'].value_counts().to_dict()
            confidence_pie_data = [{'name': k, 'value': v} for k, v in confidence_counts.items()]
            
            # Amount by category
            amount_by_category = df.groupby('category')['amount'].sum().to_dict()
            amount_chart_data = [{'name': k, 'value': v} for k, v in amount_by_category.items()]
            
            # Time series or other chart data
            chart_data = []  # Implement based on your needs
            
        return chart_data, pie_chart_data, confidence_pie_data, amount_chart_data
    except Exception as e:
        logger.error(f"Error calculating chart data: {str(e)}")
        return [], [], [], []

@app.route("/", methods=["GET", "POST"])
def index():
    try:
        if request.method == "POST":
            start_time = time.time()
            log_memory_usage()
            
            if 'invoice_file' not in request.files:
                return render_template("index.html", error="No file uploaded")

            invoice_file = request.files['invoice_file']
            
            if not invoice_file or not allowed_file(invoice_file.filename):
                return render_template("index.html", error="Please upload a valid CSV file")

            # Save file
            uploaded_filename = secure_filename(invoice_file.filename)
            invoice_path = os.path.join(app.config['UPLOAD_FOLDER'], uploaded_filename)
            invoice_file.save(invoice_path)
            os.replace(invoice_path, "data/sample_invoices.csv")

            # Clean up before ML processing
            gc.collect()
            log_memory_usage()

            try:
                # Run pipeline with memory limits
                result = subprocess.run(
                    [sys.executable, "-m", "src.pipeline"],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True,
                    timeout=300,
                    env={
                        **os.environ,
                        'PYTHONUNBUFFERED': '1',
                        'PYTHONMALLOC': 'malloc',
                        'PYTHONMALLOCSTATS': '1'
                    }
                )
                
                # Clean up after ML processing
                gc.collect()
                log_memory_usage()

                if result.returncode != 0:
                    error_msg = f"Error in processing: {result.stderr}"
                    logger.error(error_msg)
                    return render_template(
                        "index.html",
                        error=error_msg,
                        elapsed=None,
                        chart_data=[],
                        pie_chart_data=[],
                        result_table=None,
                        confidence_pie_data=[],
                        amount_chart_data=[],
                        uploaded_filename=None
                    )

                # Get results in chunks
                data = get_categorized_data()
                result_df = pd.DataFrame(data)

                if not result_df.empty:
                    # Process results in chunks
                    chunk_size = 100
                    result_table = []
                    for i in range(0, len(result_df), chunk_size):
                        chunk = result_df[i:i + chunk_size]
                        result_table.extend(chunk.to_dict(orient='records'))
                        gc.collect()

                    # Calculate chart data
                    chart_data, pie_chart_data, confidence_pie_data, amount_chart_data = calculate_chart_data(result_df)

                    return render_template(
                        "index.html",
                        result_table=result_table,
                        elapsed=time.time() - start_time,
                        chart_data=chart_data,
                        pie_chart_data=pie_chart_data,
                        confidence_pie_data=confidence_pie_data,
                        amount_chart_data=amount_chart_data,
                        uploaded_filename=uploaded_filename
                    )

            except subprocess.TimeoutExpired:
                logger.error("ML pipeline timed out")
                return render_template(
                    "index.html",
                    error="Processing took too long. Please try again with a smaller file.",
                    elapsed=None,
                    chart_data=[],
                    pie_chart_data=[],
                    result_table=None,
                    confidence_pie_data=[],
                    amount_chart_data=[],
                    uploaded_filename=None
                )
            except Exception as e:
                logger.error(f"Error in ML pipeline: {str(e)}")
                return render_template(
                    "index.html",
                    error="An error occurred during processing. Please try again.",
                    elapsed=None,
                    chart_data=[],
                    pie_chart_data=[],
                    result_table=None,
                    confidence_pie_data=[],
                    amount_chart_data=[],
                    uploaded_filename=None
                )

        return render_template("index.html")

    except Exception as e:
        logger.error(f"Error in index route: {str(e)}")
        return render_template(
            "index.html",
            error="An unexpected error occurred. Please try again.",
            elapsed=None,
            chart_data=[],
            pie_chart_data=[],
            result_table=None,
            confidence_pie_data=[],
            amount_chart_data=[],
            uploaded_filename=None
        )

@app.errorhandler(413)
def request_entity_too_large(error):
    return render_template(
        "index.html",
        error="File too large. Maximum file size is 16MB.",
        elapsed=None,
        chart_data=[],
        pie_chart_data=[],
        result_table=None,
        confidence_pie_data=[],
        amount_chart_data=[],
        uploaded_filename=None
    )

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=10000)