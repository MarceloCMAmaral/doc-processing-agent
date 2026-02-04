from langchain_google_genai import ChatGoogleGenerativeAI
from src.config import GOOGLE_API_KEY
from src.models import Invoice, ServiceContract, MaintenanceReport

def extract_data(content_data, doc_type):
    if not GOOGLE_API_KEY: return {}
    models = {"invoice": Invoice, "contract": ServiceContract, "maintenance_report": MaintenanceReport}
    target = models.get(doc_type)
    if not target: return {}
    
    llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", google_api_key=GOOGLE_API_KEY)
    structured = llm.with_structured_output(target)
    return structured.invoke(f"Extract data from: {content_data['text']}").dict()
