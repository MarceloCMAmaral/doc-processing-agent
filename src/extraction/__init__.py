from typing import Dict, Any
from .nota_fiscal_extractor import InvoiceExtractor
from .contrato_extractor import ContractExtractor
from .relatorio_extractor import ReportExtractor

def get_extractor(doc_type: str):
    extractors = {
        "invoice": InvoiceExtractor(),
        "contract": ContractExtractor(),
        "maintenance_report": ReportExtractor()
    }
    
    if doc_type not in extractors:
        raise ValueError(f"No extractor found for document type: {doc_type}")
    
    return extractors[doc_type]

def extract_data(content_data: Dict[str, Any], doc_type: str) -> Dict[str, Any]:
    """Facade function to maintain compatibility and ease of use"""
    extractor = get_extractor(doc_type)
    return extractor.extract(content_data)
