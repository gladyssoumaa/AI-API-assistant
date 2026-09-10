from __future__ import annotations

from collections import Counter
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.endpoints import APIEndpoint
from app.models.projects import Project
from app.models.user import User
from app.schemas import ProjectSummaryResponse
from app.security import get_current_user
from app.models.test_results import APITestResult

router = APIRouter(
    prefix="/projects",
    tags=["Project Summary"],
)


@router.get(
    "/{project_id}/summary",
    response_model=ProjectSummaryResponse,
)
def get_project_summary(
    project_id: UUID,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    project = (
        db.query(Project)
        .filter(
            Project.project_id == project_id,
            Project.user_id == current_user.user_id,
        )
        .first()
    )

    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found.",
        )

    endpoints = (
        db.query(APIEndpoint)
        .filter(
            APIEndpoint.project_id == project_id,
        )
        .all()
    )

    methods = Counter(
        endpoint.method.upper()
        for endpoint in endpoints
    )

    endpoint_ids = [
    endpoint.endpoint_id
    for endpoint in endpoints
    ]

    test_results = []

    if endpoint_ids:
        test_results = (
            db.query(APITestResult)
            .filter(
            APITestResult.endpoint_id.in_(endpoint_ids)
            )
            .all()
       )

    passed_tests = sum(
    1
    for result in test_results
    if result.passed
    )

    failed_tests = len(test_results) - passed_tests

    return {
        "project_id": str(project.project_id),
        "project_name": project.name,
        "endpoint_count": len(endpoints),
        "methods": dict(methods),
        "total_analyses": 0,
        "total_tests": len(test_results),
        "passed_tests": passed_tests,
        "failed_tests": failed_tests,
    }