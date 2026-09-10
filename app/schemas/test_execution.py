from pydantic import BaseModel


class TestResult(BaseModel):
    name: str
    method: str
    path: str
    expected_status_code: int
    actual_status_code: int | None
    passed: bool
    response_time_ms: float | None
    error: str | None


class TestExecutionResponse(BaseModel):
    endpoint_id: str
    total_tests: int
    passed_tests: int
    failed_tests: int
    results: list[TestResult]