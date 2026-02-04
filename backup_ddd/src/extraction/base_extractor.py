from abc import ABC, abstractmethod
from typing import Dict, Any, Type
from pydantic import BaseModel
from langchain_core.messages import HumanMessage
from langchain_google_genai import ChatGoogleGenerativeAI
from src.config.settings import GOOGLE_API_KEY
from src.utils.logger import logger
from tenacity import retry, stop_after_attempt, wait_exponential

class BaseExtractor(ABC):
    def __init__(self):
        if not GOOGLE_API_KEY:
            raise ValueError("GOOGLE_API_KEY is not set in environment variables.")
        
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-2.5-flash",
            temperature=0,
            google_api_key=GOOGLE_API_KEY
        )

    @property
    @abstractmethod
    def model(self) -> Type[BaseModel]:
        """Returns the Pydantic model for this extractor."""
        pass

    def extract(self, content_data: dict) -> Dict[str, Any]:
        """Extracts structured data from content."""
        structured_llm = self.llm.with_structured_output(self.model)
        
        user_content = []
        text = content_data.get("text", "")
        images = content_data.get("images", [])
        
        user_content.append({"type": "text", "text": "Extract the following information from the document."})
        if text:
            user_content.append({"type": "text", "text": f"\nText Content:\n{text}"})
        
        for img in images:
            user_content.append({
                "type": "image_url", 
                "image_url": {"url": f"data:{img['mime_type']};base64,{img['data']}"}
            })

        message = HumanMessage(content=user_content)

        @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10))
        def invoke_with_retry(msgs):
            return structured_llm.invoke(msgs)

        try:
            result = invoke_with_retry([message])
            logger.info(f"Extraction successful using {self.__class__.__name__}")
            return result.dict()
        except Exception as e:
            logger.error(f"Extraction failed using {self.__class__.__name__} after retries: {e}")
            raise e
