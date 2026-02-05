from typing import List
from pydantic import BaseModel, Field

class InvoiceItem(BaseModel):
    description: str
    quantity: float
    unit_value: float
    total_value: float

class Invoice(BaseModel):
    document_type: str = "invoice"
    supplier_name: str
    cnpj: str
    date: str
    items: List[InvoiceItem]
    total_amount: float

class ServiceContract(BaseModel):
    document_type: str = "contract"
    contractor_name: str
    hired_name: str
    object_description: str
    validity_date: str
    monthly_value: float

class MaintenanceReport(BaseModel):
    document_type: str = "maintenance_report"
    date: str
    technician_name: str
    equipment_name: str
    problem_description: str
    solution_description: str
