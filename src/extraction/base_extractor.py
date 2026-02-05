from abc import ABC, abstractmethod
from typing import Dict, Any

class BaseExtractor(ABC):
    @abstractmethod
    def extract(self, content_data: Dict[str, Any]) -> Dict[str, Any]:
        pass
