from dotenv import load_dotenv
from src.pipeline import run_pipeline

# Load env before importing modules
load_dotenv()

if __name__ == "__main__":
    run_pipeline()
