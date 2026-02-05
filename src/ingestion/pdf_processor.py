import os
import glob
import base64
import hashlib
from typing import List, Dict, Any
from pypdf import PdfReader
from src.config.settings import DATA_RAW_DIR

def compute_file_hash(file_path: str) -> str:
    """Computes MD5 hash of a file efficiently to detect duplicates."""
    hasher = hashlib.md5()
    with open(file_path, 'rb') as f:
        # Read in chunks of 4K to avoid memory issues with large files
        for chunk in iter(lambda: f.read(4096), b""):
            hasher.update(chunk)
    return hasher.hexdigest()

def get_pdf_files(directory: str = DATA_RAW_DIR) -> List[str]:
    """Returns a list of absolute paths to PDF files in the specified directory."""
    pattern = os.path.join(directory, "*.pdf")
    return glob.glob(pattern)

def extract_content_from_pdf(file_path: str) -> Dict[str, Any]:
    """
    Extracts content from a PDF file.
    Prioritizes text. If text is empty/insufficient, tries to extract images.
    Returns a dict with 'text' and 'images' (list of base64 strings).
    """
    try:
        reader = PdfReader(file_path)
        full_text = ""
        images_b64 = []
        
        for page in reader.pages:
            text = page.extract_text()
            if text:
                full_text += text + "\n"
            
            # Extract images if text is missing or sparse
            if len(text.strip()) < 50:
                 if page.images:
                    for img in page.images:
                        # Convert bytes to base64 for LLM consumption
                        img_b64 = base64.b64encode(img.data).decode('utf-8')
                        images_b64.append({
                            "mime_type": "image/jpeg", # Defaulting to jpeg, but strictly should check
                            "data": img_b64
                        })

        return {
            "text": full_text.strip(),
            "images": images_b64,
            "has_images": len(images_b64) > 0
        }

    except Exception as e:
        print(f"Error reading {file_path}: {e}")
        return {"text": "", "images": [], "has_images": False}

def load_documents(directory: str = DATA_RAW_DIR) -> List[Dict[str, Any]]:
    """Loads all PDFs and returns a list of dictionaries with content and metadata."""
    pdf_files = get_pdf_files(directory)
    documents = []
    
    for file_path in pdf_files:
        content_data = extract_content_from_pdf(file_path)
        documents.append({
            "content": content_data, # Now a dict with text and images
            "metadata": {
                "source": file_path,
                "filename": os.path.basename(file_path)
            }
        })
    
    return documents
