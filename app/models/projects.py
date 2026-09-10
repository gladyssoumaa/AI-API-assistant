from sqlalchemy import DateTime, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base
from typing import TYPE_CHECKING
import uuid
from datetime import datetime
if TYPE_CHECKING:
    from app.models.user import User
    from app.models.endpoints import APIEndpoint



class Project(Base):
    __tablename__ = "projects"

    project_id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True,
        default=uuid.uuid4,
        index=True,
    )

    user_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("users.user_id"),
        nullable=False,
        index=True,
    )

    name: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    description: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    base_url: Mapped[str] = mapped_column(
    String(500),
    nullable=False,
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

    owner: Mapped["User"] = relationship(
        back_populates="projects",
    )

    endpoints: Mapped[list["APIEndpoint"]] = relationship(
    "APIEndpoint",
    back_populates="project",
    cascade="all, delete-orphan",
    )