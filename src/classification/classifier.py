from langchain_core.messages import HumanMessage
from pydantic import BaseModel, Field
from langchain_google_genai import ChatGoogleGenerativeAI
from src.config.settings import GOOGLE_API_KEY
from src.config.prompts import CLASSIFICATION_SYSTEM_PROMPT
from src.utils.logger import logger
from tenacity import retry, stop_after_attempt, wait_exponential

class ClassificationResult(BaseModel):
    document_type: str = Field(
        description="The type of the document. Options: 'invoice', 'contract', 'maintenance_report', 'unknown'",
        enum=["invoice", "contract", "maintenance_report", "unknown"]
    )
    confidence: float = Field(description="Confidence score between 0 and 1")

def classify_document(content_data: dict):
    """
    Classifies the document using Gemini.
    Handles both text-only and image-based (OCR) classification.
    """
    logger.debug("Classifying document...")
    if not GOOGLE_API_KEY:
         raise ValueError("GOOGLE_API_KEY is not set in environment variables.")

    llm = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        temperature=0,
        google_api_key=GOOGLE_API_KEY
    )

    structured_llm = llm.with_structured_output(ClassificationResult)

    messages = [
        ("system", CLASSIFICATION_SYSTEM_PROMPT),
    ]

    # Construct the User Message content
    user_content = []
    
    text = content_data.get("text", "")
    images = content_data.get("images", [])
    
    if text:
        user_content.append({"type": "text", "text": f"Document Text:\n{text}"})
    
    # Add images if available (Multimodal)
    for img in images:
        user_content.append({
            "type": "image_url", 
            "image_url": {"url": f"data:{img['mime_type']};base64,{img['data']}"}
        })
        
    if not user_content:
        return None # Nothing to classify

    # Create Human Message
    messages.append(HumanMessage(content=user_content))

    # Invoke directly (PromptTemplate is tricky with multimodal lists in current LangChain versions, using messages directly is safer)
    chain = structured_llm
    
    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=2, max=10))
    def invoke_with_retry(msgs):
        return chain.invoke(msgs)

    try:
        result = invoke_with_retry(messages)
        logger.info(f"Classified as {result.document_type} (Conf: {result.confidence})")
        return result
    except Exception as e:
        logger.error(f"Classification failed after retries: {e}")
        raise e
