# run_ingest.py

import pandas as pd

# Set pandas display options to show all columns without collapsing
pd.set_option('display.max_columns', None)
pd.set_option('display.width', 1000)

from src import ingest_sanitize  # ← remove "01_" because Python module names cannot start with numbers

df = ingest_sanitize.load_and_clean("data/sample_invoices.csv")
print(df)
