from __future__ import annotations

from uuid import UUID
import json
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.analysis import APIAnalysis
from app.models.endpoints import APIEndpoint
from app.models.projects import Project
from app.models.user import User
from app.schemas.analysis import AnalysisResponse, ProjectAnalysisResponse,  TestGenerationResponse
from app.security import get_current_user
from app.services.ai import analyze_project,  analyze_endpoint, generate_tests
from app.schemas import TestExecutionResponse
from app.services.test_runner import run_api_tests
from app.models.test_results import APITestResult


router = APIRouter(
    prefix="/projects/{project_id}/endpoints",
    tags=["AI Analysis"],
)


@router.post(
    "/{endpoint_id}/analyze",
    response_model=AnalysisResponse,
)
def analyze_api_endpoint(
    project_id: UUID,
    endpoint_id: UUID,
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

    endpoint = (
        db.query(APIEndpoint)
        .filter(
            APIEndpoint.endpoint_id == endpoint_id,
            APIEndpoint.project_id == project_id,
        )
        .first()
    )

    if not endpoint:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Endpoint not found.",
        )

    try:
        result = analyze_endpoint(
            method=endpoint.method,
            path=endpoint.path,
            summary=endpoint.summary,
            description=endpoint.description,
            request_body=endpoint.request_body,
            response_body=endpoint.response_body,
            response_status_code=endpoint.response_status_code,
        )
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail=f"AI analysis failed: {exc}",
        )from exc

    analysis = APIAnalysis(
    endpoint_id=endpoint.endpoint_id,
    documentation=json.dumps(result["documentation"]),
    request_example=json.dumps(result["request_example"]),
    response_example=json.dumps(result["response_example"]),
    test_cases=json.dumps(result["test_cases"]),
    security_recommendations=json.dumps(
        result["security_recommendations"]
    ),
)

    db.add(analysis)
    db.commit()

    return result


@router.post(
    "/analyze",
    response_model=ProjectAnalysisResponse,
)
def analyze_entire_project(
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

    endpoint_data = [
        {
            "method": endpoint.method,
            "path": endpoint.path,
            "summary": endpoint.summary,
            "description": endpoint.description,
            "request_body": endpoint.request_body,
            "response_body": endpoint.response_body,
            "response_status_code": endpoint.response_status_code,
        }
        for endpoint in endpoints
    ]

    try:
        result = analyze_project(endpoint_data)
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail=f"AI project analysis failed: {exc}",
        )from exc

    return result

@router.post(
    "/{endpoint_id}/generate-tests",
    response_model=TestGenerationResponse,
)

def generate_endpoint_tests(
    project_id: UUID,
    endpoint_id: UUID,
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

    endpoint = (
        db.query(APIEndpoint)
        .filter(
            APIEndpoint.endpoint_id == endpoint_id,
            APIEndpoint.project_id == project_id,
        )
        .first()
    )

    if not endpoint:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Endpoint not found.",
        )

    try:
        tests = generate_tests(
            method=endpoint.method,
            path=endpoint.path,
            summary=endpoint.summary,
            description=endpoint.description,
            request_body=endpoint.request_body,
            response_body=endpoint.response_body,
            response_status_code=endpoint.response_status_code,
        )
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail=f"AI test generation failed: {exc}",
        )from exc

    return {
        "endpoint_id": str(endpoint.endpoint_id),
        "tests": tests,
    }

@router.post(
    "/{endpoint_id}/run-tests",
    response_model=TestExecutionResponse,
)
def run_endpoint_tests(
    project_id: UUID,
    endpoint_id: UUID,
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

    endpoint = (
        db.query(APIEndpoint)
        .filter(
            APIEndpoint.endpoint_id == endpoint_id,
            APIEndpoint.project_id == project_id,
        )
        .first()
    )

    if not endpoint:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Endpoint not found.",
        )

    try: 
        tests = generate_tests(
                method=endpoint.method,
                path=endpoint.path,
                summary=endpoint.summary,
                description=endpoint.description,
                request_body=endpoint.request_body,
                response_body=endpoint.response_body,
                response_status_code=endpoint.response_status_code,
            )
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail=f"AI test generation failed: {exc}",
        ) from exc

    results = run_api_tests(
    base_url=project.base_url,
    tests=tests,
    )

    for result in results:
        db.add(
            APITestResult(
                endpoint_id=endpoint.endpoint_id,
                name=result["name"],
                method=result["method"],
                path=result["path"],
                expected_status_code=result["expected_status_code"],
                actual_status_code=result["actual_status_code"],
                passed=result["passed"],
                response_time_ms=result["response_time_ms"],
                error=result["error"],
            )
        )

    db.commit()

    passed = sum(
    1
    for result in results
    if result["passed"]
    )

    failed = len(results) - passed
    return {
        "endpoint_id": str(endpoint.endpoint_id),
        "total_tests": len(results),
        "passed_tests": passed,
        "failed_tests": failed,
        "results": results,
    }
