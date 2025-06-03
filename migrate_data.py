# migrate_data.py
import os
import pandas as pd
import mysql.connector
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def get_db_connection():
    return mysql.connector.connect(
        host=os.getenv('DB_HOST', 'localhost'),
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASSWORD'),
        database=os.getenv('DB_NAME')
    )

def migrate_existing_data():
    try:
        # Read existing CSV files
        categorized_df = pd.read_csv('data/categorized.csv')
        manual_df = pd.read_csv('data/manual_review.csv')
        
        # Connect to database
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Migrate categorized data
        for _, row in categorized_df.iterrows():
            cursor.execute('''
                INSERT INTO categorized 
                (invoice_id, description, supplier, commodity_code, commodity_title, confidence, source)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                ON DUPLICATE KEY UPDATE
                commodity_code = VALUES(commodity_code),
                commodity_title = VALUES(commodity_title),
                confidence = VALUES(confidence)
            ''', (
                row['invoice_id'],
                row['description'],
                row['supplier'],
                row['commodity_code'],
                row['commodity_title'],
                row['confidence'],
                'CSV Migration'
            ))
        
        # Migrate manual review data
        for _, row in manual_df.iterrows():
            cursor.execute('''
                INSERT INTO manual_review 
                (invoice_id, description, supplier, commodity_code, commodity_title, confidence, source)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                ON DUPLICATE KEY UPDATE
                commodity_code = VALUES(commodity_code),
                commodity_title = VALUES(commodity_title),
                confidence = VALUES(confidence)
            ''', (
                row['invoice_id'],
                row['description'],
                row['supplier'],
                row['commodity_code'],
                row['commodity_title'],
                row['confidence'],
                'CSV Migration'
            ))
        
        conn.commit()
        print("Migration completed successfully!")
        
    except Exception as e:
        print(f"Error during migration: {str(e)}")
        conn.rollback()
    finally:
        cursor.close()
        conn.close()

if __name__ == "__main__":
    print("Starting data migration...")
    migrate_existing_data()
    print("Migration process completed!")