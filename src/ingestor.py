import os
import glob
from pypdf import PdfReader

def get_pdf_files(directory):
    return glob.glob(os.path.join(directory, "*.pdf"))

def extract_content_from_pdf(file_path):
    try:
        reader = PdfReader(file_path)
        text = ""
        for page in reader.pages:
            text += page.extract_text() + "\n"
        return {"text": text, "images": []}
    except Exception as e:
        print(f"Error: {e}")
        return {"text": "", "images": []}

def load_documents():
    from src.config import DATA_RAW_DIR
    files = get_pdf_files(DATA_RAW_DIR)
    docs = []
    for f in files:
        docs.append({"content": extract_content_from_pdf(f), "metadata": {"filename": os.path.basename(f)}})
    return docs
