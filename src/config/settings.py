import os
from dotenv import load_dotenv

load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

DATA_RAW_DIR = os.path.join(os.getcwd(), "data", "raw")
DATA_PROCESSED_DIR = os.path.join(os.getcwd(), "data", "processed")
DATA_QUARANTINE_DIR = os.path.join(os.getcwd(), "data", "quarantine")
DATA_HASHES_FILE = os.path.join(DATA_PROCESSED_DIR, "hashes.json")
