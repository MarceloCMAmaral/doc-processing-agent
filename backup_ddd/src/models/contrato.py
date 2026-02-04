from pydantic import BaseModel, Field

class ServiceContract(BaseModel):
    document_type: str = Field(default="contract", description="Type of the document")
    contractor_name: str = Field(description="Name of the contractor (Part requesting service)")
    hired_name: str = Field(description="Name of the hired party (Service provider)")
    object_description: str = Field(description="Description of the object of the contract")
    validity_date: str = Field(description="Validity date or duration of the contract")
    monthly_value: float = Field(description="Monthly value of the contract")
