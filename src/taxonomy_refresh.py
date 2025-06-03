import schedule
import time
import os
from src.taxonomy_service import fetch_unspsc
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def job():
    try:
        logger.info("Starting taxonomy refresh job...")
        df = fetch_unspsc()
        logger.info(f"Refreshed UNSPSC: {len(df)} codes loaded.")
    except Exception as e:
        logger.error(f"Error in taxonomy refresh: {str(e)}")

if __name__ == '__main__':
    # Run once at startup
    job()
    
    # Schedule the job
    schedule.every(24).hours.do(job)
    
    # Keep the script running
    while True:
        schedule.run_pending()
        time.sleep(60)