import pandas as pd
import re

def load_and_clean(path: str) -> pd.DataFrame:
    """
    Reads invoice CSV, normalizes headers, lowercases & cleans description text,
    drops rows missing key fields, and removes duplicates.
    Keeps all original columns.
    """
    df = pd.read_csv(path, dtype=str)
    df.columns = [c.strip().lower().replace(' ', '_') for c in df.columns]

    def clean(s):
        s = (s or '').strip().lower()
        return re.sub(r'[^\x00-\x7F]+', ' ', s)

    if 'description' in df.columns:
        df['description'] = df['description'].apply(clean)

    df = df.dropna(subset=['supplier', 'sku', 'description'])
    df = df.drop_duplicates()

    return df
