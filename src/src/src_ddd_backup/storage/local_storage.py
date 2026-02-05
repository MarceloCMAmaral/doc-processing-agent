import os
import json
import pandas as pd
from typing import List, Dict
from src.config.settings import DATA_PROCESSED_DIR
from src.utils.logger import logger

def save_result(filename: str, result: Dict):
    """Saves the extraction result to a JSON file."""
    base_name = os.path.splitext(filename)[0]
    output_path = os.path.join(DATA_PROCESSED_DIR, f"{base_name}.json")
    
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=4, ensure_ascii=False)
    logger.info(f"[SAVED] {output_path}")

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
                logger.error(f"Error reading {filename} for consolidation: {e}")
                
    return data_list

def consolidate_to_csv(output_path: str = "consolidated_results.csv"):
    """Consolidates processed data into a single CSV file."""
    data = load_processed_data()
    
    if not data:
        logger.warning("No processed data found to consolidate.")
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
    logger.info(f"[SUCCESS] Consolidated {len(df)} records to {output_path}")
