from dotenv import load_dotenv
from src.pipeline.orchestrator import DocumentPipeline

# Load env before anything else
load_dotenv()

def main():
    pipeline = DocumentPipeline()
    pipeline.run()

if __name__ == "__main__":
    main()
