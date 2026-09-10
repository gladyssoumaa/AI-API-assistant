from pydantic import BaseModel
from typing import Any

class AnalysisResponse(BaseModel):
    documentation: Any
    request_example: Any
    response_example: Any
    test_cases: list[Any]
    security_recommendations: list[Any]