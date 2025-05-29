import logging, multiprocessing as mp
import pandas as pd
from src.ingest_sanitize import load_and_clean
from src.rule_filter import apply_rules
from src.retrieval import shortlist
from src.genai_inference import classify_with_ai
from src.taxonomy_service import unspsc_map

# Configure logging
logging.basicConfig(filename='logs/pipeline.log', level=logging.INFO,
                    format='%(asctime)s %(levelname)s %(message)s')
CONF_THRESH = 0.85
DATA_PATH   = 'data/sample_invoices.csv'

# Helper for parallel row processing
def process_row(r):
    desc, supp = r['description'], r['supplier']
    info = apply_rules(desc)
    src  = 'rule' if info else 'genai'
    if not info:
        cand = shortlist(desc)
        info = classify_with_ai(desc, supp, cand)
    rec = {**r.to_dict(), **info, 'source':src}
    target = 'manual' if info['confidence']<CONF_THRESH else 'final'
    return target, rec

# Main pipeline
def run_pipeline():
    df = load_and_clean(DATA_PATH)
    final, manual = [], []
    for _, r in df.iterrows():
        tgt, rec = process_row(r)
        (manual if tgt=='manual' else final).append(rec)
    pd.DataFrame(final).to_csv('data/categorized.csv',index=False)
    pd.DataFrame(manual).to_csv('data/manual_review.csv',index=False)
    logging.info(f"Pipeline done: {len(final)} final, {len(manual)} manual")

if __name__=='__main__': run_pipeline()