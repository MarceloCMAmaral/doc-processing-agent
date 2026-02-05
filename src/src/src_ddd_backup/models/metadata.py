from pydantic import BaseModel

class DocumentMetadata(BaseModel):
    filename: str
    file_path: str
    predicted_type: str
