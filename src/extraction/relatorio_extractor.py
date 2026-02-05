from typing import Dict, Any
from langchain_core.messages import HumanMessage
from langchain_google_genai import ChatGoogleGenerativeAI
from tenacity import retry, stop_after_attempt, wait_exponential

from src.extraction.base_extractor import BaseExtractor
from src.models.relatorio import MaintenanceReport
from src.config.settings import GOOGLE_API_KEY
from src.config.prompts import EXTRACTION_SYSTEM_PROMPT
from src.utils.logger import logger

class ReportExtractor(BaseExtractor):
    def extract(self, content_data: Dict[str, Any]) -> Dict[str, Any]:
        if not GOOGLE_API_KEY:
            raise ValueError("GOOGLE_API_KEY is not set.")

        logger.info("Extracting Report data...")
        
        llm = ChatGoogleGenerativeAI(
            model="gemini-2.5-flash",
            temperature=0,
            google_api_key=GOOGLE_API_KEY
        )
        
        structured_llm = llm.with_structured_output(MaintenanceReport)
        
        user_content = []
        user_content.append({"type": "text", "text": EXTRACTION_SYSTEM_PROMPT})
        
        text = content_data.get("text", "")
        images = content_data.get("images", [])

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
            logger.info("Report extraction successful.")
            return result.dict()
        except Exception as e:
            logger.error(f"Report extraction failed: {e}")
            raise e
