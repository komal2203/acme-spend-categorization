import streamlit as st
import pandas as pd
import os
import subprocess
import altair as alt
import matplotlib.pyplot as plt
import plotly.express as px
import sys  # <-- Add this import

st.set_page_config(page_title='Invoice Categorization Results', layout='wide')
st.markdown("""
    <h1 style='text-align: center; color: #4F8BF9; margin-bottom: 2rem;'>
        📄 Invoice Categorization Results
    </h1>
""", unsafe_allow_html=True)

# --- Upload and Run Model Section ---
uploaded_file = st.file_uploader(
    "Upload a CSV file containing your invoice or spend data for categorization:",
    type=["csv"],
    help="Upload a CSV file with invoice data. This will overwrite the current sample_invoices.csv."
)



model_ran = False

if uploaded_file is not None:
    with open("data/sample_invoices.csv", "wb") as f:
        f.write(uploaded_file.getbuffer())
    # st.success("File uploaded! Click 'Run Model' to process.")

st.markdown("<div style='margin-top: 1.5rem;'></div>", unsafe_allow_html=True)
col1, col2, col3 = st.columns([2, 1, 2])
with col2:
    run_model = st.button("🚀 Run Model")  # or your preferred emoji/text

if run_model:
    if not os.path.exists("data/sample_invoices.csv"):
        st.error("Please upload a sample_invoices.csv file first.")
        st.stop()
    # Center the "Categorizing..." message horizontally using columns
    col1, col2, col3 = st.columns([2, 1, 2])
    with col2:
        msg_placeholder = st.empty()
        msg_placeholder.markdown(
            "<div style=' font-size:1.2rem; color:#4F8BF9;'>Categorizing...</div>",
            unsafe_allow_html=True
        )
        result = subprocess.run(
            [sys.executable, "-m", "src.pipeline"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        msg_placeholder.empty()
    if result.returncode == 0:
        st.success("Categorization complete! See results below.")
        model_ran = True
    else:
        st.error("There was an error running the model:")
        st.code(result.stderr)
        st.stop()

# --- Results Section ---
if (run_model and model_ran) or (
    os.path.exists('data/sample_invoices.csv') and os.path.exists('data/categorized.csv') and run_model
):
    input_df = pd.read_csv('data/sample_invoices.csv')
    output_df = pd.read_csv('data/categorized.csv')

    # Normalize column names for matching
    input_df.columns = [c.lower().replace(' ', '_') for c in input_df.columns]
    output_df.columns = [c.lower().replace(' ', '_') for c in output_df.columns]

    # Merge on invoice_id (adjust if your key is different)
    if 'invoice_id' in input_df.columns and 'invoice_id' in output_df.columns:
        merged = pd.merge(input_df, output_df, on='invoice_id', suffixes=('_input', '_output'))
    else:
        st.error("Could not find 'invoice_id' column in both files for merging.")
        st.stop()

    # Remove redundant output columns (keep only unique output columns)
    redundant_cols = [col for col in merged.columns if col.endswith('_output') and col.replace('_output', '_input') in merged.columns]

    # Dynamically map input columns to their merged names (with _input suffix if present)
    input_cols = []
    for col in input_df.columns:
        if col in merged.columns:
            input_cols.append(col)
        elif f"{col}_input" in merged.columns:
            input_cols.append(f"{col}_input")

    # Key output columns to display (remove unwanted columns)
    key_output_cols = [
        'commodity_code', 'commodity_title', 'confidence',  'source', 'matched_rule'
    ]
    final_cols = input_cols + [col for col in key_output_cols if col in merged.columns]

    filtered = merged.copy()

    # Rename columns for display
    rename_dict = {
        'commodity_code': 'UNSPSC Category ID',
        'commodity_title': 'UNSPSC Category Name'
    }
    # Remove _input suffix from input columns for display
    clean_cols = [col[:-6] if col.endswith('_input') else col for col in filtered[final_cols].columns]
    display_df = filtered[final_cols].copy()
    display_df.columns = clean_cols
    display_df = display_df.rename(columns=rename_dict)
    
     #Remove any unwanted index columns if present
    if 'index' in display_df.columns:
        display_df = display_df.drop(columns=['index'])
    if 'Unnamed: 0' in display_df.columns:
        display_df = display_df.drop(columns=['Unnamed: 0'])

    # Show summary stats in columns
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Invoices", len(merged))
    col2.metric("Filtered", len(filtered))
    if 'confidence' in filtered.columns:
        avg_conf = filtered['confidence'].mean()
        col3.metric("Avg. Confidence", f"{avg_conf:.2f}")
    else:
        col3.write("")

    st.markdown("---")

    # Subheader and download button in one row
    left_col, right_col = st.columns([3, 1])
    with left_col:
        st.subheader("Invoices with Categorization")
    with right_col:
        st.download_button(
            label="⬇️ Download Results as CSV",
            data=display_df.to_csv(index=False),
            file_name="categorized_invoices.csv",
            mime="text/csv"
        )

    # Display the results in a nice table
    st.dataframe(display_df.reset_index(drop=True), use_container_width=True, height=500)

    # --- Data Visualizations ---
    st.markdown("## 📊 Data Visualizations")

    # 1. Bar chart: Top 10 UNSPSC Categories
    # 1. Bar chart: Top 10 UNSPSC Categories
    if 'UNSPSC Category Name' in display_df.columns:
        st.subheader("Top 10 UNSPSC Categories")
        cat_series = display_df['UNSPSC Category Name'].    value_counts().head(10)
        if not cat_series.empty:
            top_categories = cat_series.reset_index()
            top_categories.columns = ['Category', 'Count']
            chart = alt.Chart(top_categories).mark_bar().encode (
                x=alt.X('Category:N', sort='-y'),
                y='Count:Q'
            )
            st.altair_chart(chart, use_container_width=True)
        else:
            st.info("No category data available for bar chart.")
    else:
        st.info("'UNSPSC Category Name' column not found in results.")

    # 2. Pie chart: Invoice Distribution of Top 5 Categories
    if 'UNSPSC Category Name' in display_df.columns:
        st.subheader("Invoice Distribution of Top 5 Categories")
        cat_counts = display_df['UNSPSC Category Name'].value_counts().head(5)
        if not cat_counts.empty:
            fig, ax = plt.subplots()
            ax.pie(cat_counts, labels=cat_counts.index, autopct='%1.1f%%', startangle=90)
            ax.axis('equal')
            st.pyplot(fig)
        else:
            st.info("No category data available for pie chart.")

    # 3. Histogram: Confidence Score Distribution (optional)
    # if 'confidence' in display_df.columns and pd.api.types.is_numeric_dtype(display_df['confidence']):
    #     st.subheader("Distribution of Confidence Scores")
    #     st.bar_chart(display_df['confidence'])

    # 4. Treemap: Invoice Hierarchy (optional, update columns as needed)
    # treemap_cols = ['segment_title', 'family_title', 'class_title', 'UNSPSC Category Name']
    # if set(treemap_cols).issubset(display_df.columns) and not display_df.empty:
    #     treemap_df = display_df.dropna(subset=treemap_cols)
    #     if not treemap_df.empty:
    #         st.subheader("Invoice Hierarchy Treemap")
    #         fig = px.treemap(
    #             treemap_df,
    #             path=treemap_cols,
    #             title="Invoice Categorization Treemap"
    #         )
    #         st.plotly_chart(fig, use_container_width=True)
    #     else:
    #         st.info("Not enough data for treemap (missing values in hierarchy columns).")