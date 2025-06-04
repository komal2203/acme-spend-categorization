import logging
import pandas as pd
import time
import gc
import psutil 
import sys
import os
from src.ingest_sanitize import load_and_clean
from src.rule_filter import apply_rules
from src.retrieval import shortlist
from src.genai_inference import classify_with_ai
from src.taxonomy_service import unspsc_map

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
CHUNK_SIZE = 10

# Read and check the input file
df = pd.read_csv('data/sample_invoices.csv')
print("Columns in file:", df.columns.tolist())
print("\nFirst few rows:")
print(df.head())

def process_single_row(row):
    """Process a single row"""
    try:
        # Use correct column names (capitalized)
        desc = row['Description']
        supp = row['Supplier']
        
        info = apply_rules(desc)
        return info
    except Exception as e:
        logger.error(f"Error processing row: {str(e)}")
        raise

def save_chunk_results(final_chunk, manual_chunk, is_first_chunk=False):
    """Save chunk results to CSV files"""
    try:
        # Create data directory if it doesn't exist
        os.makedirs('data', exist_ok=True)
        
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

def run_pipeline():
    """Main pipeline"""
    try:
        total_start = time.time()
        logger.info("Starting pipeline...")

        # Load and clean data
        t0 = time.time()
        df = load_and_clean(DATA_PATH)
        logger.info(f"Data loading/cleaning took {time.time() - t0:.2f} seconds")
        logger.info(f"Loaded data shape: {df.shape}")
        logger.info(f"Columns: {df.columns.tolist()}")

        # Process in chunks
        total_final = 0
        total_manual = 0
        is_first_chunk = True

        for chunk in pd.read_csv(DATA_PATH, chunksize=CHUNK_SIZE):
            # Process chunk
            t1 = time.time()
            final_chunk, manual_chunk = [], []
            
            for _, row in chunk.iterrows():
                result = process_single_row(row)
                if result[0] == 'manual':
                    manual_chunk.append(result[1])
                else:
                    final_chunk.append(result[1])
            
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

            is_first_chunk = False

        # Log final statistics
        logger.info(f"Pipeline completed:")
        logger.info(f"- Total final records: {total_final}")
        logger.info(f"- Total manual review records: {total_manual}")
        logger.info(f"- Total pipeline time: {time.time() - total_start:.2f} seconds")

    except Exception as e:
        logger.error(f"Error in pipeline: {str(e)}")
        raise

if __name__ == '__main__':
    try:
        run_pipeline()
    except Exception as e:
        logger.error(f"Pipeline failed: {str(e)}")
        sys.exit(1)