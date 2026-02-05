import os
import json
import time
import concurrent.futures
from typing import Dict

from src.config.settings import DATA_PROCESSED_DIR
from src.utils.logger import logger
from src.ingestion.pdf_processor import load_documents
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
        content_data = doc["content"]
        
        logger.info(f"Processing: {filename}")
        
        # Idempotency Check
        base_name = os.path.splitext(filename)[0]
        output_path = os.path.join(DATA_PROCESSED_DIR, f"{base_name}.json")
        if os.path.exists(output_path):
            logger.info(f"Skipping {filename} (Already processed)")
            return "skipped"

        # Empty Content Check
        if not content_data["text"] and not content_data["images"]:
            logger.warning(f"Skipping {filename} (No text/images)")
            return "error"

        try:
            # 1. Classification
            classification = classify_document(content_data)
            
            if not classification:
                logger.warning(f"Could not classify {filename}")
                return "error"

            doc_type = classification.document_type
            confidence = classification.confidence
            
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
        
        stats = {"invoice": 0, "contract": 0, "maintenance_report": 0, "unknown": 0, "skipped": 0, "error": 0}
        
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
