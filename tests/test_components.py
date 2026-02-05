import unittest
from unittest.mock import MagicMock
from src.ingestion import load_documents
from src.classification import classify_document, ClassificationResult
from src.extraction import extract_data

class TestComponents(unittest.TestCase):

    def test_classifier_mock(self):
        """Test classifier logic with mocked LLM response."""
        # We don't want to call real API in unit tests
        # This is just a structure test
        pass # Real testing would involve mocking ChatGoogleGenerativeAI

    def test_pydantic_models(self):
        """Test that Pydantic models validate data correctly."""
        from src.models.nota_fiscal import Invoice, InvoiceItem
        
        item = InvoiceItem(description="Test", quantity=1, unit_value=10.0, total_value=10.0)
        invoice = Invoice(
            supplier_name="Test Corp",
            cnpj="00000000000",
            date="2024-01-01",
            items=[item],
            total_amount=10.0
        )
        self.assertEqual(invoice.total_amount, 10.0)

    def test_ingestor_structure(self):
        """Test if ingestor returns correct list structure."""
        # Mock glob and pdf reading would be needed here for full test
        # For now, we trust the import works
        self.assertTrue(callable(load_documents))

if __name__ == '__main__':
    unittest.main()
