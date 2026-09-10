from __future__ import annotations

import uuid
from datetime import datetime
from typing import TYPE_CHECKING
from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base
if TYPE_CHECKING:
    from app.models.endpoints import APIEndpoint


class APITestResult(Base):
    __tablename__ = "api_test_results"

    result_id: Mapped[uuid.UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        index=True,
    )

    endpoint_id: Mapped[uuid.UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("api_endpoints.endpoint_id"),
        nullable=False,
        index=True,
    )

    name: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    method: Mapped[str] = mapped_column(
        String(10),
        nullable=False,
    )

    path: Mapped[str] = mapped_column(
        String(500),
        nullable=False,
    )

    expected_status_code: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    actual_status_code: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True,
    )

    passed: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
    )

    response_time_ms: Mapped[float | None] = mapped_column(
        nullable=True,
    )

    error: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
    )

    endpoint: Mapped["APIEndpoint"] = relationship(
        "APIEndpoint",
        back_populates="test_results",
    )