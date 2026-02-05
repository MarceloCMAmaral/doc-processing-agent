from typing import List
from pydantic import BaseModel, Field, model_validator

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

    @model_validator(mode='after')
    def check_math(self):
        """Validates if the sum of items matches the total amount."""
        calculated_total = sum(item.total_value for item in self.items)
        # Tolerance of 0.01 for floating point rounding errors
        if abs(calculated_total - self.total_amount) > 0.01:
             print(f"[WARNING] Math divergence detected! Calculated: {calculated_total:.2f}, Note Total: {self.total_amount:.2f}")
             # We could add a warning flag here if the model supported it
        return self
