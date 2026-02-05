import os
import json
import pandas as pd
from typing import List, Dict
from src.config.settings import DATA_PROCESSED_DIR

def load_processed_data() -> List[Dict]:
    """Loads all JSON files from the processed directory."""
    data_list = []
    
    if not os.path.exists(DATA_PROCESSED_DIR):
        return []

    for filename in os.listdir(DATA_PROCESSED_DIR):
        if filename.endswith(".json"):
            filepath = os.path.join(DATA_PROCESSED_DIR, filename)
            try:
                with open(filepath, "r", encoding="utf-8") as f:
                    content = json.load(f)
                    
                    # Flatten logic: Combine metadata and data
                    flat_entry = content.get("metadata", {}).copy()
                    
                    # Handle classification hierarchy flatten
                    if "classification" in flat_entry:
                        flat_entry["doc_type"] = flat_entry["classification"].get("type")
                        flat_entry["confidence"] = flat_entry["classification"].get("confidence")
                        del flat_entry["classification"]
                    
                    # Add extraction data
                    extracted_data = content.get("data")
                    if extracted_data:
                        # Prefix data fields to avoid collision
                        for k, v in extracted_data.items():
                            if isinstance(v, list):
                                flat_entry[f"data_{k}"] = json.dumps(v, ensure_ascii=False) # Store lists as JSON string in CSV
                            else:
                                flat_entry[f"data_{k}"] = v
                    
                    data_list.append(flat_entry)
            except Exception as e:
                print(f"Error reading {filename}: {e}")
                
    return data_list

def consolidate_to_csv(output_path: str = "consolidated_results.csv"):
    """Consolidates processed data into a single CSV file."""
    data = load_processed_data()
    
    if not data:
        print("No processed data found to consolidate.")
        return

    df = pd.DataFrame(data)
    
    # Reorder columns for better readability (Filename first)
    cols = ['filename', 'doc_type', 'confidence', 'processed_at', 'status']
    # Add remaining columns that are not in the fixed list
    cols += [c for c in df.columns if c not in cols]
    
    # Filter only existing columns
    cols = [c for c in cols if c in df.columns]
    
    df = df[cols]
    
    df.to_csv(output_path, index=False, encoding="utf-8-sig") # utf-8-sig for Excel compatibility
    print(f"[SUCCESS] Consolidated {len(df)} records to {output_path}")
