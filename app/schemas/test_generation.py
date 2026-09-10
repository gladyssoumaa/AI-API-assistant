from pydantic import BaseModel


class GeneratedTest(BaseModel):
    name: str
    description: str
    method: str
    path: str
    expected_status_code: int


class TestGenerationResponse(BaseModel):
    endpoint_id: str
    tests: list[GeneratedTest]