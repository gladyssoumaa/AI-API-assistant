from pydantic import BaseModel


class FailureAnalysisResponse(BaseModel):
    summary: str
    failures: list[str]
    recommendations: list[str]