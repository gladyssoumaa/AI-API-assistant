from pydantic import BaseModel
from typing import Any

class AnalysisResponse(BaseModel):
    documentation: Any
    request_example: Any
    response_example: Any
    test_cases: Any
    security_recommendations: Any


class ProjectAnalysisResponse(BaseModel):
    project_overview: Any
    documentation: Any
    test_strategy: Any
    security_recommendations: Any
    issues_found: Any

class TestGenerationResponse(BaseModel):
    endpoint_id: str
    tests: Any


class TestExecutionResponse(BaseModel):
    endpoint_id: str
    total_tests: int
    passed_tests: int
    failed_tests: int
    results: list[Any]