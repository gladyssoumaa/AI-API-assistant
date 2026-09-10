from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.projects import Project
from app.models.user import User
from app.security import require_admin

router = APIRouter(
    prefix="/admin",
    tags=["Administration"],
)


@router.get("/users")
def get_users(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin),
):
    users = db.query(User).order_by(
        User.created_at.desc()
    ).all()

    return [
        {
            "user_id": str(user.user_id),
            "email": user.email,
            "role": user.role,
            "created_at": user.created_at,
        }
        for user in users
    ]


@router.get("/projects")
def get_all_projects(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin),
):
    projects = db.query(Project).order_by(
        Project.created_at.desc()
    ).all()

    return [
        {
            "project_id": str(project.project_id),
            "user_id": str(project.user_id),
            "name": project.name,
            "description": project.description,
            "base_url": project.base_url,
            "created_at": project.created_at,
        }
        for project in projects
    ]


@router.get("/statistics")
def get_statistics(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin),
):
    total_users = db.query(User).count()
    total_projects = db.query(Project).count()

    return {
        "total_users": total_users,
        "total_projects": total_projects,
    }