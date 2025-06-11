import schedule
import time
import os
from src.taxonomy_service import fetch_unspsc

# Ensure the data directory exists (if fetch_unspsc writes to disk)
os.makedirs("data", exist_ok=True)

def job():
    df = fetch_unspsc()
    print(f"[{time.ctime()}] Refreshed UNSPSC: {len(df)} codes loaded.")

# Schedule the job every 24 hours
schedule.every(90).days.do(job)

if __name__ == '__main__':
    job()  # Run once at startup
    while True:
        schedule.run_pending()
        time.sleep(60)