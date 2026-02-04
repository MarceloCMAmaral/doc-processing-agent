from typing import Type
from pydantic import BaseModel
from .base_extractor import BaseExtractor
from src.models.contrato import ServiceContract

class ContractExtractor(BaseExtractor):
    @property
    def model(self) -> Type[BaseModel]:
        return ServiceContract
