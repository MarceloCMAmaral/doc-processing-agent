from src.ingestor import load_documents
from src.classifier import classify_document
from src.extractor import extract_data
import json
import os

def main():
    print("Starting MVP Pipeline...")
    docs = load_documents()
    for doc in docs:
        print(f"Processing {doc['metadata']['filename']}")
        cls = classify_document(doc['content'])
        if cls:
            print(f"Type: {cls.document_type}")
            data = extract_data(doc['content'], cls.document_type)
            with open(f"data/processed/{doc['metadata']['filename']}.json", "w") as f:
                json.dump(data, f)

if __name__ == "__main__":
    main()
