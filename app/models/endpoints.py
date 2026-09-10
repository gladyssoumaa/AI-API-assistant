from __future__ import annotations
import uuid
from datetime import datetime
from typing import TYPE_CHECKING
from sqlalchemy import DateTime, ForeignKey, String, Text
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base

if TYPE_CHECKING:
    from app.models.projects import Project
    from app.models.analysis import APIAnalysis
    from app.models.test_results import APITestResult


class APIEndpoint(Base):
    __tablename__ = "api_endpoints"

    endpoint_id: Mapped[uuid.UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        index=True,
    )

    project_id: Mapped[uuid.UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("projects.project_id"),
        nullable=False,
        index=True,
    )

    method: Mapped[str] = mapped_column(
        String(10),
        nullable=False,
    )

    path: Mapped[str] = mapped_column(
        String(500),
        nullable=False,
    )

    summary: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )

    description: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    request_body: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    response_body: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    response_status_code: Mapped[int | None] = mapped_column(
        nullable=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False,
    )

    project: Mapped["Project"] = relationship(
        "Project",
        back_populates="endpoints",
    )

    analyses: Mapped[list["APIAnalysis"]] = relationship(
        "APIAnalysis",
        back_populates="endpoint",
        cascade="all, delete-orphan",
    )

    test_results: Mapped[list["APITestResult"]] = relationship(
    "APITestResult",
    back_populates="endpoint",
    cascade="all, delete-orphan",
)