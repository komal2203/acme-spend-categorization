import os
import pandas as pd
from flask import Flask, render_template, request, send_from_directory, redirect
from werkzeug.utils import secure_filename
import subprocess
import sys
import time
from src.taxonomy_service import unspsc_map
from src.taxonomy_service import unspsc_dropdown_map

UPLOAD_FOLDER = 'uploads'
RESULTS_FOLDER = 'results'
ALLOWED_EXTENSIONS = {'csv'}

app = Flask(__name__)

# # Start Streamlit server when Flask app starts
# subprocess.Popen(["streamlit", "run", "src/manual_review.py"], shell=True)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['RESULTS_FOLDER'] = RESULTS_FOLDER

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(RESULTS_FOLDER, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# @app.route("/manual_review")
# def manual_review():
#     # Start the Streamlit server programmatically
#     subprocess.Popen(["streamlit", "run", "src/manual_review.py"], shell=True)
#     # Redirect to the Streamlit interface
#     return redirect("http://localhost:8501")  # Replace with the Streamlit URL



# @app.route("/manual_review", methods=["GET", "POST"])
# def manual_review():
#     manual_review_path = "data/manual_review.csv"

#     # Check if the manual review file exists
#     if not os.path.exists(manual_review_path):
#         return render_template("manual_review.html", data=[], unspsc_map=unspsc_dropdown_map, error="No manual review records found.")

#     df = pd.read_csv(manual_review_path)

#     if request.method == "POST":
#         # Handle corrections submitted by the user
#         invoice_id = request.form.get("invoice_id")
#         corrected_code = request.form.get("corrected_code")
#         df.loc[df["invoice_id"] == int(invoice_id), "commodity_code"] = corrected_code
#         df.loc[df["invoice_id"] == int(invoice_id), "confidence"] = 1.0
#         df.to_csv(manual_review_path, index=False)
#         return render_template("manual_review.html", data=df.to_dict(orient="records"), unspsc_map=unspsc_dropdown_map, success=True)

#     return render_template("manual_review.html", data=df.to_dict(orient="records"), unspsc_map=unspsc_dropdown_map)

@app.route("/download_categorized")
def download_categorized():
    return send_from_directory(directory="data", path="categorized.csv", as_attachment=True)

# @app.route("/manual_review", methods=["GET", "POST"])
# def manual_review():
#     from src.taxonomy_service import unspsc_dropdown_map  # Import the simplified dropdown map
#     manual_review_path = "data/manual_review.csv"
#     categorized_path = "data/categorized.csv"

#     # Ensure categorized.csv exists
#     if not os.path.exists(categorized_path):
#         pd.DataFrame(columns=["invoice_id", "description", "commodity_code", "confidence"]).to_csv(categorized_path, index=False)

#     # Check if the manual review file exists
#     if not os.path.exists(manual_review_path):
#         return render_template("manual_review.html", data=[], unspsc_map=unspsc_dropdown_map, error="No manual review records found.")

#     df = pd.read_csv(manual_review_path)
    
#     if df.empty:
#         return render_template("manual_review.html", data=[], unspsc_map=unspsc_dropdown_map, error="No invoices for manual review!")

#     if request.method == "POST":
#         # Handle corrections submitted by the user
#         invoice_id = int(request.form.get("invoice_id"))
#         corrected_code = request.form.get("corrected_code")

#         # Find the row to save
#         row_to_save = df[df["invoice_id"] == invoice_id].copy()
#         row_to_save["commodity_code"] = corrected_code
#         row_to_save["confidence"] = 1.0

#         # Append the row to categorized.csv
#         categorized_df = pd.read_csv(categorized_path)
#         categorized_df = pd.concat([categorized_df, row_to_save], ignore_index=True)
#         categorized_df.to_csv(categorized_path, index=False)

#         # Remove the row from manual_review.csv
#         df = df[df["invoice_id"] != invoice_id]
#         df.to_csv(manual_review_path, index=False)

#         return render_template(
#             "manual_review.html",
#             data=df.to_dict(orient="records"),
#             unspsc_map=unspsc_dropdown_map,
#             success=True,
#             download_link="/download_categorized"
#         )

#     return render_template(
#         "manual_review.html",
#         data=df.to_dict(orient="records"),
#         unspsc_map=unspsc_dropdown_map
#     )
    
    
# @app.route("/manual_review", methods=["GET", "POST"])
# def manual_review():
#     from src.taxonomy_service import unspsc_dropdown_map  # Import the dropdown map
#     manual_review_path = "data/manual_review.csv"

#     # Check if the manual review file exists
#     if not os.path.exists(manual_review_path):
#         return render_template("manual_review.html", data=[], unspsc_map=unspsc_dropdown_map, error="No invoices to review!")

#     # Read the file into a DataFrame
#     df = pd.read_csv(manual_review_path)

#     # Check if the file is empty
#     if df.empty:
#         return render_template("manual_review.html", data=[], unspsc_map=unspsc_dropdown_map, error="No invoices to review!")

#     # Handle POST requests for corrections
#     if request.method == "POST":
#         invoice_id = int(request.form.get("invoice_id"))
#         corrected_code = request.form.get("corrected_code")

#         # Find the row to save
#         row_to_save = df[df["invoice_id"] == invoice_id].copy()
#         row_to_save["commodity_code"] = corrected_code
#         row_to_save["confidence"] = 1.0

#         # Append the row to categorized.csv
#         categorized_path = "data/categorized.csv"
#         categorized_df = pd.read_csv(categorized_path)
#         categorized_df = pd.concat([categorized_df, row_to_save], ignore_index=True)
#         categorized_df.to_csv(categorized_path, index=False)

#         # Remove the row from manual_review.csv
#         df = df[df["invoice_id"] != invoice_id]
#         df.to_csv(manual_review_path, index=False)

#         return render_template(
#             "manual_review.html",
#             data=df.to_dict(orient="records"),
#             unspsc_map=unspsc_dropdown_map,
#             success=True,
#             download_link="/download_categorized"
#         )

#     # Render the manual review page with data
#     return render_template(
#         "manual_review.html",
#         data=df.to_dict(orient="records"),
#         unspsc_map=unspsc_dropdown_map
#     )
    
    
@app.route("/manual_review", methods=["GET", "POST"])
def manual_review():
    from src.taxonomy_service import unspsc_dropdown_map  # Import the dropdown map
    manual_review_path = "data/manual_review.csv"

    # Check if the manual review file exists
    if not os.path.exists(manual_review_path):
        return render_template("manual_review.html", data=[], unspsc_map=unspsc_dropdown_map, error="No invoices to review!")

    try:
        # Read the file into a DataFrame
        df = pd.read_csv(manual_review_path)

        # Check if the file is empty
        if df.empty:
            return render_template("manual_review.html", data=[], unspsc_map=unspsc_dropdown_map, error="No invoices to review!")
    except pd.errors.EmptyDataError:
        # Handle completely empty files (no rows and no columns)
        return render_template("manual_review.html", data=[], unspsc_map=unspsc_dropdown_map, error="No invoices to review!")

    # Handle POST requests for corrections
    if request.method == "POST":
        invoice_id = int(request.form.get("invoice_id"))
        corrected_code = request.form.get("corrected_code")

        # Find the row to save
        row_to_save = df[df["invoice_id"] == invoice_id].copy()
        row_to_save["commodity_code"] = corrected_code
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
            unspsc_map=unspsc_dropdown_map,
            success=True,
            download_link="/download_categorized"
        )

    # Render the manual review page with data
    return render_template(
        "manual_review.html",
        data=df.to_dict(orient="records"),
        unspsc_map=unspsc_dropdown_map
    )
    
@app.route("/", methods=["GET", "POST"])
def index():
    result_table = None
    chart_data = []
    pie_chart_data = []
    error = None
    elapsed = None

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
                result_table=result_table
            )

        invoice_path = os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(invoice_file.filename))
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
                result_table=result_table
            )

        # Load results
        result_df = pd.read_csv("data/categorized.csv")
        result_df.columns = [c.strip().lower().replace(' ', '_') for c in result_df.columns]

        # Prepare chart data BEFORE renaming columns for display
        commodity_col = next((c for c in result_df.columns if 'commodity_title' in c), None)
        if commodity_col and not result_df.empty:
            result_df = result_df.dropna(subset=[commodity_col])
            
            # Adjust the number of top categories for the bar graph
            top_n = 15  # Change this number to adjust the number of top categories
            vc_df = result_df[commodity_col].value_counts().nlargest(top_n).reset_index()
            cat_col = vc_df.columns[0]
            count_col = vc_df.columns[1]
            chart_data = (
                vc_df.rename(columns={cat_col: 'category', count_col: 'count'})
                .to_dict(orient='records')
            )
            
            # Prepare pie chart data for top 5 commodity_titles
            pie_vc_df = result_df[commodity_col].value_counts().nlargest(5).reset_index()
            pie_cat_col = pie_vc_df.columns[0]
            pie_count_col = pie_vc_df.columns[1]
            pie_chart_data = (
                pie_vc_df.rename(columns={pie_cat_col: 'category', pie_count_col: 'count'})
                .to_dict(orient='records')
            )
        else:
            chart_data = []
            pie_chart_data = []

        # Remove unnecessary columns for display
        cols_to_remove = [
            'segment_code', 'segment_title',
            'family_code', 'family_title',
            'class_code', 'class_title'
        ]
        result_df = result_df.drop(columns=[c for c in cols_to_remove if c in result_df.columns])

        result_table = result_df.to_html(classes="result-table", index=False)

        return render_template(
            "index.html",
            result_table=result_table,
            elapsed=elapsed,
            chart_data=chart_data,
            pie_chart_data=pie_chart_data,
        )

    # For GET requests, just render the page with no results
    return render_template(
        "index.html",
        result_table=result_table,
        elapsed=elapsed,
        chart_data=chart_data,
        pie_chart_data=pie_chart_data
    )

@app.route("/download")
def download():
    # Adjust the path if your output file is elsewhere
    return send_from_directory(directory="data", path="categorized.csv", as_attachment=True)


@app.route("/download_manual")
def download_manual():
    # Adjust the path if your output file is elsewhere
    return send_from_directory(directory="data", path="manual_review.csv", as_attachment=True)
if __name__ == "__main__":
    app.run(debug=True)
    
