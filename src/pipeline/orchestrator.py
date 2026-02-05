import os
import json
import time
import concurrent.futures
import shutil
import threading
from typing import Dict, Set

from src.config.settings import DATA_PROCESSED_DIR, DATA_QUARANTINE_DIR, DATA_HASHES_FILE
from src.utils.logger import logger
from src.ingestion.pdf_processor import load_documents, compute_file_hash
from src.classification.classifier import classify_document
from src.extraction.nota_fiscal_extractor import InvoiceExtractor
from src.extraction.contrato_extractor import ContractExtractor
from src.extraction.relatorio_extractor import ReportExtractor
from src.pipeline.consolidator import consolidate_to_csv

class DocumentPipeline:
    def __init__(self):
        self.extractors = {
            "invoice": InvoiceExtractor(),
            "contract": ContractExtractor(),
            "maintenance_report": ReportExtractor()
        }
        self.lock = threading.Lock()
        self.processed_hashes = self._load_hashes()

    def _load_hashes(self) -> Set[str]:
        """Loads processed file hashes from disk."""
        if os.path.exists(DATA_HASHES_FILE):
             try:
                 with open(DATA_HASHES_FILE, 'r') as f:
                     return set(json.load(f))
             except Exception as e:
                 logger.error(f"Failed to load hashes file: {e}")
                 return set()
        return set()

    def _save_hash(self, file_hash: str):
        """Thread-safe generic method to save a new hash."""
        with self.lock:
            self.processed_hashes.add(file_hash)
            try:
                # For safety, we write the whole set.
                # In high volume, append-only would be better, but this is fine for now.
                with open(DATA_HASHES_FILE, 'w') as f:
                    json.dump(list(self.processed_hashes), f)
            except Exception as e:
                logger.error(f"Failed to save hash registry: {e}")

    def save_result(self, filename: str, result: Dict):
        """Saves the extraction result to a JSON file."""
        os.makedirs(DATA_PROCESSED_DIR, exist_ok=True)
        base_name = os.path.splitext(filename)[0]
        output_path = os.path.join(DATA_PROCESSED_DIR, f"{base_name}.json")
        
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(result, f, indent=4, ensure_ascii=False)
        logger.info(f"[SAVED] {output_path}")

    def process_document(self, doc: Dict) -> str:
        """
        Processes a single document. Returns the document type processed (or 'error').
        """
        filename = doc["metadata"]["filename"]
        source_path = doc["metadata"]["source"] # Getting source path
        content_data = doc["content"]
        
        logger.info(f"Processing: {filename}")
        
        # 0. Duplicity Check (Hash-based)
        try:
            file_hash = compute_file_hash(source_path)
            with self.lock:
                if file_hash in self.processed_hashes:
                    logger.info(f"Skipping {filename} (Duplicate Content - Hash: {file_hash})")
                    return "skipped_duplicate"
        except Exception as e:
            logger.error(f"Error computing hash for {filename}: {e}")
            # Continue processing if hash fails, or return error?
            # Let's verify by proceeding, but log error.
        
        # Idempotency Check (Filename-based) - Legacy but kept for double safety
        base_name = os.path.splitext(filename)[0]
        output_path = os.path.join(DATA_PROCESSED_DIR, f"{base_name}.json")
        if os.path.exists(output_path):
            logger.info(f"Skipping {filename} (Already processed file)")
            return "skipped"

        # Empty Content Check
        if not content_data["text"] and not content_data["images"]:
            logger.warning(f"Skipping {filename} (No text/images extracted). Moving to Quarantine.")
            
            # Move to quarantine as "Unreadable"
            os.makedirs(DATA_QUARANTINE_DIR, exist_ok=True)
            dest_path = os.path.join(DATA_QUARANTINE_DIR, filename)
            try:
                shutil.move(source_path, dest_path)
                logger.info(f"[QUARANTINE] Moved {filename} to {DATA_QUARANTINE_DIR} (Reason: Unreadable/Empty)")
                return "quarantined_unreadable"
            except Exception as e:
                logger.error(f"Failed to move {filename} to quarantine: {e}")
                return "error"

        try:
            # 1. Classification
            classification = classify_document(content_data)
            
            if not classification:
                logger.warning(f"Could not classify {filename}")
                return "error"

            doc_type = classification.document_type
            confidence = classification.confidence
            
            # 1.5 Quarantine Check (Human-in-the-Loop)
            if confidence < 0.80:
                logger.warning(f"Low confidence ({confidence:.2f}) for {filename}. Moving to quarantine.")
                
                os.makedirs(DATA_QUARANTINE_DIR, exist_ok=True)
                dest_path = os.path.join(DATA_QUARANTINE_DIR, filename)
                
                try:
                    # Copy then delete, or move. shutil.move handles cross-fs.
                    shutil.move(source_path, dest_path)
                    logger.info(f"[QUARANTINE] Moved {filename} to {DATA_QUARANTINE_DIR}")
                    return "quarantined"
                except Exception as e:
                    logger.error(f"Failed to move {filename} to quarantine: {e}")
                    return "error"

            # 2. Handle Unknown
            if doc_type == "unknown":
                logger.warning(f"Document {filename} identified as UNKNOWN/ANOMALOUS")
                output = {
                    "metadata": {
                        "filename": filename,
                        "processed_at": time.strftime("%Y-%m-%d %H:%M:%S"),
                        "classification": {
                            "type": doc_type,
                            "confidence": confidence
                        },
                        "status": "skipped_unknown"
                    },
                    "data": None
                }
                self.save_result(filename, output)
                # We also save hash for unknown? Maybe. Let's say yes to avoid re-evaluating unknown files.
                self._save_hash(file_hash)
                return "unknown"

            # 3. Extraction
            extractor = self.extractors.get(doc_type)
            if not extractor:
                logger.error(f"No extractor found for type: {doc_type}")
                return "error"

            data = extractor.extract(content_data)
            
            # 4. Persistence
            output = {
                "metadata": {
                    "filename": filename,
                    "processed_at": time.strftime("%Y-%m-%d %H:%M:%S"),
                    "classification": {
                        "type": doc_type,
                        "confidence": confidence
                    }
                },
                "data": data
            }
            
            self.save_result(filename, output)
            
            # 5. Success - Register Hash
            self._save_hash(file_hash)
            
            return doc_type

        except Exception as e:
            logger.error(f"Failed to process {filename}: {e}", exc_info=True)
            return "error"

    def run(self):
        logger.info("--- Starting Document Processing Pipeline (Parallel) ---")
        
        # 1. Ingestion
        logger.info("Step 1: Ingesting documents...")
        documents = load_documents()
        logger.info(f"Found {len(documents)} documents.")

        if not documents:
            logger.warning("No documents found in data/raw.")
            return

        # 2. Parallel Processing Loop
        logger.info("Step 2: Processing documents in parallel...")
        
        stats = {
            "invoice": 0, 
            "contract": 0, 
            "maintenance_report": 0, 
            "unknown": 0, 
            "skipped": 0, 
            "skipped_duplicate": 0,
            "quarantined": 0,
            "error": 0
        }
        
        # Max workers = 5 to avoid Rate Limits on Gemini API
        MAX_WORKERS = 5
        
        with concurrent.futures.ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
            # Start all tasks
            future_to_file = {executor.submit(self.process_document, doc): doc["metadata"]["filename"] for doc in documents}
            
            for future in concurrent.futures.as_completed(future_to_file):
                filename = future_to_file[future]
                try:
                    result_type = future.result()
                    if result_type in stats:
                        stats[result_type] += 1
                    else:
                        stats["error"] += 1
                except Exception as e:
                    logger.error(f"Generated an exception for {filename}: {e}")
                    stats["error"] += 1

        logger.info("--- Processing Complete ---")
        logger.info("Summary:")
        for k, v in stats.items():
            logger.info(f"  {k}: {v}")
        
        logger.info("Step 3: Consolidating results...")
        consolidate_to_csv()
