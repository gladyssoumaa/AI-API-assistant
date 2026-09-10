from __future__ import annotations

import uuid
from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, ForeignKey, Text
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base

if TYPE_CHECKING:
    from app.models.endpoints import APIEndpoint
    from app.models.analysis import APIAnalysis


class APIAnalysis(Base):
    __tablename__ = "api_analyses"

    analysis_id: Mapped[uuid.UUID] = mapped_column(
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

    documentation: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    request_example: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    response_example: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    test_cases: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    security_recommendations: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
    )

    endpoint: Mapped["APIEndpoint"] = relationship(
        "APIEndpoint",
        back_populates="analyses",
    )

    