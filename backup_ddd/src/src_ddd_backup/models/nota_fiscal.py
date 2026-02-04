from typing import List
from pydantic import BaseModel, Field

class InvoiceItem(BaseModel):
    description: str = Field(description="Description of the item or service")
    quantity: float = Field(description="Quantity of the item")
    unit_value: float = Field(description="Unit value of the item")
    total_value: float = Field(description="Total value of the item")

class Invoice(BaseModel):
    document_type: str = Field(default="invoice", description="Type of the document")
    supplier_name: str = Field(description="Name of the supplier or issuer")
    cnpj: str = Field(description="CNPJ of the supplier")
    date: str = Field(description="Date of emission or document validity")
    items: List[InvoiceItem] = Field(description="List of items in the invoice")
    total_amount: float = Field(description="Total amount of the invoice")
