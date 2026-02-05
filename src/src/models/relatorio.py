from pydantic import BaseModel, Field

class MaintenanceReport(BaseModel):
    document_type: str = Field(default="maintenance_report", description="Type of the document")
    date: str = Field(description="Date of the maintenance report")
    technician_name: str = Field(description="Name of the technician responsible")
    equipment_name: str = Field(description="Name/ID of the equipment maintained")
    problem_description: str = Field(description="Description of the problem reported")
    solution_description: str = Field(description="Description of the solution applied")
