from pydantic import BaseModel


class ProjectAnalysisResponse(BaseModel):
    project_overview: str
    documentation: str
    test_strategy: list[str]
    security_recommendations: list[str]
    issues_found: list[str]