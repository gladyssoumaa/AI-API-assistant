from __future__ import annotations

from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.endpoints import APIEndpoint
from app.models.projects import Project
from app.models.user import User
from app.schemas.endpoints import (
    EndpointCreate,
    EndpointResponse,
    EndpointUpdate,
)
from app.security import get_current_user

router = APIRouter(
    prefix="/projects/{project_id}/endpoints",
    tags=["API Endpoints"],
)


def get_owned_project(
    project_id: UUID,
    current_user: User,
    db: Session,
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

    return project


@router.post(
    "",
    response_model=EndpointResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_endpoint(
    project_id: UUID,
    endpoint_data: EndpointCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    get_owned_project(
        project_id,
        current_user,
        db,
    )

    endpoint = APIEndpoint(
        project_id=project_id,
        method=endpoint_data.method.upper(),
        path=endpoint_data.path,
        summary=endpoint_data.summary,
        description=endpoint_data.description,
        request_body=endpoint_data.request_body,
        response_body=endpoint_data.response_body,
        response_status_code=endpoint_data.response_status_code,
    )

    db.add(endpoint)
    db.commit()
    db.refresh(endpoint)

    return endpoint

@router.get(
    "",
    response_model=list[EndpointResponse],
)
def list_endpoints(
    project_id: UUID,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    get_owned_project(
        project_id,
        current_user,
        db,
    )

    return (
        db.query(APIEndpoint)
        .filter(
            APIEndpoint.project_id == project_id,
        )
        .order_by(APIEndpoint.created_at.desc())
        .all()
    )

@router.get(
    "/{endpoint_id}",
    response_model=EndpointResponse,
)
def get_endpoint(
    project_id: UUID,
    endpoint_id: UUID,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    get_owned_project(
        project_id,
        current_user,
        db,
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

    return endpoint

@router.put(
    "/{endpoint_id}",
    response_model=EndpointResponse,
)
def update_endpoint(
    project_id: UUID,
    endpoint_id: UUID,
    endpoint_data: EndpointUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    get_owned_project(
        project_id,
        current_user,
        db,
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

    update_data = endpoint_data.model_dump(
        exclude_unset=True,
    )

    if "method" in update_data:
        update_data["method"] = update_data["method"].upper()

    for field, value in update_data.items():
        setattr(endpoint, field, value)

    db.commit()
    db.refresh(endpoint)

    return endpoint

@router.delete(
    "/{endpoint_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_endpoint(
    project_id: UUID,
    endpoint_id: UUID,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    get_owned_project(
        project_id,
        current_user,
        db,
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

    db.delete(endpoint)
    db.commit()