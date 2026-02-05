from typing import Type
from pydantic import BaseModel
from .base_extractor import BaseExtractor
from src.models.relatorio import MaintenanceReport

class ReportExtractor(BaseExtractor):
    @property
    def model(self) -> Type[BaseModel]:
        return MaintenanceReport
