import os
from pypdf import PdfReader
from src.config import DATA_RAW_DIR

def analyze_pdf(filename):
    path = os.path.join(DATA_RAW_DIR, filename)
    print(f"Analyzing: {path}")
    
    try:
        reader = PdfReader(path)
        print(f"Pages: {len(reader.pages)}")
        
        page = reader.pages[0]
        text = page.extract_text()
        print(f"Text length: {len(text)}")
        if len(text) < 50:
             print(f"Text preview: '{text}'")
        
        print("\nChecking for images...")
        images = page.images
        print(f"Images found on page 0: {len(images)}")
        for img in images:
            print(f"  Image: {img.name}, Data length: {len(img.data)}")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    # Pick the first one from the list we saw earlier
    analyze_pdf("001_pjpo.pdf")
