import logging, multiprocessing as mp
import pandas as pd
from src.ingest_sanitize import load_and_clean
from src.rule_filter import apply_rules
from src.retrieval import shortlist
from src.genai_inference import classify_with_ai
from src.taxonomy_service import unspsc_map
import time
import logging
import concurrent.futures

logging.basicConfig(level=logging.INFO)

# Configure logging
logging.basicConfig(filename='logs/pipeline.log', level=logging.INFO,
                    format='%(asctime)s %(levelname)s %(message)s')
CONF_THRESH = 0.85
DATA_PATH   = 'data/sample_invoices.csv'

# Helper for parallel row processing
def process_row(r):
    import time
    desc, supp = r['description'], r['supplier']
    t0 = time.time()
    info = apply_rules(desc)
    rule_time = time.time() - t0

    src  = 'Rule' if info else 'GenAI'
    shortlist_time = 0
    genai_time = 0

    if not info:
        t1 = time.time()
        cand = shortlist(desc)
        shortlist_time = time.time() - t1

        t2 = time.time()
        info = classify_with_ai(desc, supp, cand)
        genai_time = time.time() - t2

    rec = {**r.to_dict(), **info, 'source':src}
    target = 'manual' if info['confidence']<CONF_THRESH else 'final'

    # Log timings for this row
    logging.info(f"Row timings - rule: {rule_time:.2f}s, shortlist: {shortlist_time:.2f}s, genai: {genai_time:.2f}s")
    return target, rec

# Main pipeline

def run_pipeline():
    total_start = time.time()
    t0 = time.time()
    df = load_and_clean(DATA_PATH)
    print("Running pipeline...")
    logging.info(f"Data loading/cleaning took {time.time() - t0:.2f} seconds")
    t1 = time.time()
    final, manual = [], []
    logging.info(f"Business rule application took {time.time() - t1:.2f} seconds")

    t2 = time.time()
    # Use ThreadPoolExecutor for parallel GenAI calls
    with concurrent.futures.ThreadPoolExecutor(max_workers=30) as executor:
        results = list(executor.map(process_row, [r for _, r in df.iterrows()]))
    for tgt, rec in results:
        (manual if tgt=='manual' else final).append(rec)
    logging.info(f"GenAI inference took {time.time() - t2:.2f} seconds")

    t3 = time.time()
    pd.DataFrame(final).to_csv('data/categorized.csv',index=False)
    pd.DataFrame(manual).to_csv('data/manual_review.csv',index=False)
    logging.info(f"Pipeline done: {len(final)} final, {len(manual)} manual")
    logging.info(f"Output writing took {time.time() - t3:.2f} seconds")
    logging.info(f"Total pipeline time: {time.time() - total_start:.2f} seconds")
    
if __name__=='__main__': run_pipeline()