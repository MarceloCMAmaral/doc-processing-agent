from langchain_google_genai import ChatGoogleGenerativeAI
from src.config import GOOGLE_API_KEY
from pydantic import BaseModel, Field

class ClassificationResult(BaseModel):
    document_type: str = Field(enum=["invoice", "contract", "maintenance_report"])
    confidence: float

def classify_document(content_data):
    if not GOOGLE_API_KEY: return None
    llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", google_api_key=GOOGLE_API_KEY)
    structured = llm.with_structured_output(ClassificationResult)
    # Simplified prompt for MVP
    return structured.invoke(f"Classify this text: {content_data['text']}")
