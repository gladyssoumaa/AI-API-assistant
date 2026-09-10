from pydantic import BaseModel


class ProjectSummaryResponse(BaseModel):
    project_id: str
    project_name: str
    endpoint_count: int
    methods: dict[str, int]
    total_analyses: int
    total_tests: int
    passed_tests: int
    failed_tests: int