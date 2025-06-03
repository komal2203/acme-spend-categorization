import sys
import os

# Add your project directory to Python path
path = '/home/komalmeena220303/acme-spend-categorization'
if path not in sys.path:
    sys.path.append(path)

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

# Import your Flask app
from app import app as application