from typing import Type
from pydantic import BaseModel
from .base_extractor import BaseExtractor
from src.models.nota_fiscal import Invoice

class InvoiceExtractor(BaseExtractor):
    @property
    def model(self) -> Type[BaseModel]:
        return Invoice
