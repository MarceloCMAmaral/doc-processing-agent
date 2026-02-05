CLASSIFICATION_SYSTEM_PROMPT = """You are an expert document classifier. 
Analyze the provided document (text or image) and categorize it into one of the following types:

1. **invoice**: Contains supplier info, CNPJ, list of items, values, total. (Nota Fiscal)
2. **contract**: Contains parties (contractor/hired), object, validity, monthly value. (Contrato de Prestação de Serviços)
3. **maintenance_report**: Contains date, technician, equipment, problem, solution. (Relatório de Manutenção)
4. **unknown**: If the document does NOT fit any of the above categories or is illegible/corrupted.

Return the classification and a confidence score.
"""

EXTRACTION_SYSTEM_PROMPT = "Extract the following information from the document."
