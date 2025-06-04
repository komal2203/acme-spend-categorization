import logging
import multiprocessing as mp
import pandas as pd
import time
import gc
import psutil 
import sys
from src.ingest_sanitize import load_and_clean
from src.rule_filter import apply_rules
from src.retrieval import shortlist
from src.genai_inference import classify_with_ai
from src.taxonomy_service import unspsc_map
import concurrent.futures

# Configure logging
logging.basicConfig(
    filename='logs/pipeline.log',
    level=logging.INFO,
    format='%(asctime)s %(levelname)s %(message)s'
)
logger = logging.getLogger(__name__)

# Constants
CONF_THRESH = 0.85
DATA_PATH = 'data/sample_invoices.csv'
CHUNK_SIZE = 10  # Smaller chunks
MAX_WORKERS = 2  # Fewer workers

# Cache model
model = None
def get_model():
    global model
    if model is None:
        model = load_model()  # Load once
    return model

def check_memory_usage():
    process = psutil.Process(os.getpid())
    memory_info = process.memory_info()
    memory_mb = memory_info.rss / 1024 / 1024
    if memory_mb > 400:  # Alert before hitting 512MB limit
        logger.warning(f"High memory usage: {memory_mb:.2f} MB")
    return memory_mb

def process_single_row(row):
    """Process a single row with memory optimization"""
    try:
        desc, supp = row['description'], row['supplier']
        t0 = time.time()
        
        # Apply rules
        info = apply_rules(desc)
        rule_time = time.time() - t0

        src = 'Rule' if info else 'GenAI'
        shortlist_time = 0
        genai_time = 0

        if not info:
            t1 = time.time()
            cand = shortlist(desc)
            shortlist_time = time.time() - t1

            t2 = time.time()
            info = classify_with_ai(desc, supp, cand)
            genai_time = time.time() - t2

        rec = {**row.to_dict(), **info, 'source': src}
        target = 'manual' if info['confidence'] < CONF_THRESH else 'final'

        # Log timings
        logger.info(f"Row timings - rule: {rule_time:.2f}s, shortlist: {shortlist_time:.2f}s, genai: {genai_time:.2f}s")
        
        return target, rec

    except Exception as e:
        logger.error(f"Error processing row: {str(e)}")
        raise

def process_chunk(chunk):
    try:
        final, manual = [], []
        memory_before = check_memory_usage()
        
        with concurrent.futures.ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
            results = list(executor.map(process_single_row, [r for _, r in chunk.iterrows()]))
        
        memory_after = check_memory_usage()
        logger.info(f"Memory change: {memory_after - memory_before:.2f} MB")
        
        for tgt, rec in results:
            (manual if tgt == 'manual' else final).append(rec)
        
        return final, manual
    except Exception as e:
        logger.error(f"Error processing chunk: {str(e)}")
        raise

def save_chunk_results(final_chunk, manual_chunk, is_first_chunk=False):
    """Save chunk results to CSV files"""
    try:
        # Save final results
        if not final_chunk.empty:
            final_chunk.to_csv(
                'data/categorized.csv',
                mode='w' if is_first_chunk else 'a',
                header=is_first_chunk,
                index=False
            )
        
        # Save manual review results
        if not manual_chunk.empty:
            manual_chunk.to_csv(
                'data/manual_review.csv',
                mode='w' if is_first_chunk else 'a',
                header=is_first_chunk,
                index=False
            )
            
    except Exception as e:
        logger.error(f"Error saving chunk results: {str(e)}")
        raise

def process_row(row):
    result = process_single_row(row)
    gc.collect()  # Clean after each row
    return result

def process_file(file_path):
    for chunk in pd.read_csv(file_path, chunksize=10):
        yield process_chunk(chunk)

def run_pipeline():
    """Main pipeline with memory optimization"""
    try:
        total_start = time.time()
        logger.info("Starting pipeline...")
        initial_memory = check_memory_usage()
        logger.info(f"Initial memory usage: {initial_memory:.2f} MB")

        # Load and clean data
        t0 = time.time()
        df = load_and_clean(DATA_PATH)
        logger.info(f"Data loading/cleaning took {time.time() - t0:.2f} seconds")
        logger.info(f"Memory after loading: {check_memory_usage():.2f} MB")

        # Process in chunks
        total_final = 0
        total_manual = 0
        is_first_chunk = True

        for chunk in pd.read_csv(DATA_PATH, chunksize=CHUNK_SIZE):
            # Process chunk
            t1 = time.time()
            final_chunk, manual_chunk = process_chunk(chunk)
            logger.info(f"Chunk processing took {time.time() - t1:.2f} seconds")

            # Save results
            t2 = time.time()
            save_chunk_results(
                pd.DataFrame(final_chunk),
                pd.DataFrame(manual_chunk),
                is_first_chunk
            )
            logger.info(f"Chunk saving took {time.time() - t2:.2f} seconds")

            # Update counts
            total_final += len(final_chunk)
            total_manual += len(manual_chunk)

            # Clean up
            del final_chunk, manual_chunk
            gc.collect()
            logger.info(f"Memory after cleanup: {check_memory_usage():.2f} MB")

            is_first_chunk = False

        # Log final statistics
        final_memory = check_memory_usage()
        logger.info(f"Pipeline completed:")
        logger.info(f"- Total final records: {total_final}")
        logger.info(f"- Total manual review records: {total_manual}")
        logger.info(f"- Total pipeline time: {time.time() - total_start:.2f} seconds")
        logger.info(f"- Final memory usage: {final_memory:.2f} MB")
        logger.info(f"- Memory change: {final_memory - initial_memory:.2f} MB")

    except Exception as e:
        logger.error(f"Error in pipeline: {str(e)}")
        raise

def save_results(results):
    with open('results.csv', 'a') as f:
        for result in results:
            f.write(f"{result}\n")

def log_memory():
    process = psutil.Process()
    memory = process.memory_info().rss / 1024 / 1024
    logger.info(f"Memory usage: {memory:.2f} MB")

if __name__ == '__main__':
    try:
        run_pipeline()
    except Exception as e:
        logger.error(f"Pipeline failed: {str(e)}")
        sys.exit(1)