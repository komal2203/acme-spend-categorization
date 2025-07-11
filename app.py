import os
import pandas as pd
from flask import Flask, render_template, request, send_from_directory, redirect
from werkzeug.utils import secure_filename
import subprocess
import sys
import time
from src.taxonomy_service import unspsc_map
from src.taxonomy_service import unspsc_dropdown_map
from src.evaluation_metrics import generate_evaluation_report

def prettify_column(col):
    # Remove underscores, capitalize each word, join with space
    return ' '.join(word.capitalize() for word in col.split('_'))

UPLOAD_FOLDER = 'uploads'
RESULTS_FOLDER = 'results'
ALLOWED_EXTENSIONS = {'csv'}

app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['RESULTS_FOLDER'] = RESULTS_FOLDER

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(RESULTS_FOLDER, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/manual_review", methods=["GET", "POST"])
def manual_review():
    manual_review_path = "data/manual_review.csv"

    # Check if the manual review file exists
    if not os.path.exists(manual_review_path):
        return render_template(
            "manual_review.html",
            data=[],
            unspsc_dropdown_map=unspsc_dropdown_map,
            error="No invoices to review!"
        )

    try:
        # Read the file into a DataFrame
        df = pd.read_csv(manual_review_path)

        # Check if the file is empty
        if df.empty:
            return render_template(
                "manual_review.html",
                data=[],
                unspsc_dropdown_map=unspsc_dropdown_map,
                error="No invoices to review!"
            )
    except pd.errors.EmptyDataError:
        return render_template(
            "manual_review.html",
            data=[],
            unspsc_dropdown_map=unspsc_dropdown_map,
            error="No invoices to review!"
        )

    # Handle POST requests for corrections
    if request.method == "POST":
        invoice_id = int(request.form.get("invoice_id"))
        corrected_code = request.form.get("corrected_code")

        # Find the row to save
        row_to_save = df[df["invoice_id"] == invoice_id].copy()
        row_to_save["commodity_code"] = corrected_code
        # Add the commodity title from the dropdown map
        row_to_save["commodity_title"] = unspsc_dropdown_map.get(corrected_code, "")
        row_to_save["confidence"] = 1.0

        # Append the row to categorized.csv
        categorized_path = "data/categorized.csv"
        categorized_df = pd.read_csv(categorized_path)
        categorized_df = pd.concat([categorized_df, row_to_save], ignore_index=True)
        categorized_df.to_csv(categorized_path, index=False)

        # Remove the row from manual_review.csv
        df = df[df["invoice_id"] != invoice_id]
        df.to_csv(manual_review_path, index=False)

        return render_template(
            "manual_review.html",
            data=df.to_dict(orient="records"),
            unspsc_dropdown_map=unspsc_dropdown_map,
            success=True,
            download_link="/download_categorized"
        )

    # Render the manual review page with data
    return render_template(
        "manual_review.html",
        data=df.to_dict(orient="records"),
        unspsc_dropdown_map=unspsc_dropdown_map
    )

# @app.route("/download_categorized")
# def download_categorized():
#     return send_from_directory(directory="data", path="categorized.csv", as_attachment=True)

@app.route("/download_updated_csv")
def download_updated_csv():
    try:
        # Read both files
        manual_df = pd.read_csv("data/manual_review.csv")
        categorized_df = pd.read_csv("data/categorized.csv")
        
        # Combine the dataframes
        combined_df = pd.concat([manual_df, categorized_df], ignore_index=True)
        
        # Create a temporary file
        temp_file = "data/updated_classifications.csv"
        combined_df.to_csv(temp_file, index=False)
        
        return send_file(
            temp_file,
            mimetype='text/csv',
            as_attachment=True,
            download_name='updated_classifications.csv'
        )
    except Exception as e:
        return str(e), 500
    
@app.route("/download_categorized")
def download_categorized():
    df = pd.read_csv("data/categorized.csv")
    
    # Ensure commodity_title exists and is correct
    if 'commodity_title' not in df.columns:
        df['commodity_title'] = df['commodity_code'].map(unspsc_dropdown_map)

    df.columns = [prettify_column(c) for c in df.columns]
    # Remove the Confidence Rounded column if it exists
    if 'Confidence Rounded' in df.columns:
        df = df.drop(columns=['Confidence Rounded'])
    df = df.rename(columns={
        "Commodity Title": "UNSPSC Category Name",  # Removed \n
        "Commodity Code": "UNSPSC Category ID"      # Removed \n
    })
    # Save the modified DataFrame to a temporary file
    temp_path = "data/temp_categorized.csv"
    df.to_csv(temp_path, index=False)
    try:
        return send_from_directory(directory="data", path="temp_categorized.csv", as_attachment=True)
    finally:
        # Clean up the temporary file
        try:
            os.remove(temp_path)
        except:
            pass

@app.route("/download_manual")
def download_manual():
    return send_from_directory(directory="data", path="manual_review.csv", as_attachment=True)

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
    evaluation_report = {}

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
                uploaded_filename=uploaded_filename,
                evaluation_report=evaluation_report
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
                uploaded_filename=uploaded_filename,
                evaluation_report=evaluation_report
            )

        try:
            # Read the categorized data
            df = pd.read_csv("data/categorized.csv")
            
            # Generate evaluation metrics
            evaluation_report = generate_evaluation_report(df)
            
            # Prepare confidence pie data
            confidence_col = 'confidence'
            source_col = 'source'
            
            if confidence_col in df.columns and not df.empty:
                temp_df = df.copy()
                temp_df['Confidence Rounded'] = temp_df[confidence_col].round(4)
                confidence_counts = temp_df.groupby(['Confidence Rounded', source_col]).size().reset_index(name='count')
                confidence_pie_data = []
                for _, row in confidence_counts.iterrows():
                    confidence_pie_data.append({
                        'category': row['Confidence Rounded'],
                        'count': row['count'],
                        'source': row[source_col]
                    })
            
            # Now prettify other columns for display
            result_df = df.copy()
            result_df.columns = [prettify_column(c) for c in result_df.columns]
            
            # Remove the Confidence Rounded column if it exists
            if 'Confidence Rounded' in result_df.columns:
                result_df = result_df.drop(columns=['Confidence Rounded'])
            
            # Explicitly rename the two columns
            result_df = result_df.rename(columns={
                "Commodity Title": "UNSPSC\nCategory\nName",
                "Commodity Code": "UNSPSC \nCategory ID\n"
            })
            
            # Prepare chart data
            commodity_col = "UNSPSC\nCategory\nName"
            if commodity_col in result_df.columns and not result_df.empty:
                result_df = result_df.dropna(subset=[commodity_col])
                top_n = 10
                vc_df = result_df[commodity_col].value_counts().nlargest(top_n).reset_index()
                cat_col = vc_df.columns[0]
                count_col = vc_df.columns[1]
                chart_data = (
                    vc_df.rename(columns={cat_col: 'category', count_col: 'count'})
                    .to_dict(orient='records')
                )
            
            # Prepare supplier pie chart data
            supplier_col = "Supplier"
            if supplier_col in result_df.columns and not result_df.empty:
                pie_vc_df = result_df[supplier_col].value_counts().nlargest(5).reset_index()
                pie_sup_col = pie_vc_df.columns[0]
                pie_count_col = pie_vc_df.columns[1]
                pie_chart_data = (
                    pie_vc_df.rename(columns={pie_sup_col: 'category', pie_count_col: 'count'})
                    .to_dict(orient='records')
                )
            
            # Prepare amount chart data
            amount_col = "Amount"
            if amount_col in result_df.columns and supplier_col in result_df.columns and not result_df.empty:
                result_df[amount_col] = (
                    result_df[amount_col]
                    .astype(str)
                    .replace(r'[\$,]', '', regex=True)
                    .replace('', '0')
                    .astype(float)
                )
                amount_by_supplier = (
                    result_df.groupby(supplier_col)[amount_col]
                    .sum()
                    .nlargest(10)
                    .reset_index()
                )
                amount_chart_data = amount_by_supplier.rename(
                    columns={supplier_col: "category", amount_col: "amount"}
                ).to_dict(orient="records")
            
            # Remove unnecessary columns
            cols_to_remove = [
                'Segment Code', 'Segment Title',
                'Family Code', 'Family Title',
                'Class Code', 'Class Title'
            ]
            result_df = result_df.drop(columns=[c for c in cols_to_remove if c in result_df.columns])
            
            result_table = result_df.to_html(classes="result-table", index=False)
            
        except Exception as e:
            print(f"Error processing results: {str(e)}")
            error = f"Error processing results: {str(e)}"
            return render_template(
                "index.html",
                error=error,
                elapsed=elapsed,
                chart_data=chart_data,
                pie_chart_data=pie_chart_data,
                result_table=result_table,
                amount_chart_data=amount_chart_data,
                confidence_pie_data=confidence_pie_data,
                uploaded_filename=uploaded_filename,
                evaluation_report=evaluation_report
            )

    return render_template(
        "index.html",
        result_table=result_table,
        elapsed=elapsed,
        chart_data=chart_data,
        pie_chart_data=pie_chart_data,
        confidence_pie_data=confidence_pie_data,
        amount_chart_data=amount_chart_data,
        uploaded_filename=uploaded_filename,
        evaluation_report=evaluation_report
    )

@app.route("/download")
def download():
    df = pd.read_csv("data/categorized.csv")
    df.columns = [prettify_column(c) for c in df.columns]
    # Remove the Confidence Rounded column if it exists
    if 'Confidence Rounded' in df.columns:
        df = df.drop(columns=['Confidence Rounded'])
    df = df.rename(columns={
        "Commodity Title": "UNSPSC\nCategory\nName",
        "Commodity Code": "UNSPSC \nCategory ID\n"
    })
    # temp_path = "data/categorized_pretty.csv"
    # df.to_csv(temp_path, index=False)
    # return send_from_directory(directory="data", path="categorized_pretty.csv", as_attachment=True)

     # Save the modified DataFrame to a temporary file
    temp_path = "data/temp_categorized.csv"
    df.to_csv(temp_path, index=False)
    return send_from_directory(directory="data", path="temp_categorized.csv", as_attachment=True)

if __name__ == "__main__":
    app.run(debug=False)