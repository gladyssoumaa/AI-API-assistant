from __future__ import annotations
from datetime import datetime
import uuid
from pydantic import BaseModel, ConfigDict, EmailStr



class ProjectBase(BaseModel):
    name: str
    description: str | None = None
    base_url: str


class ProjectCreate(ProjectBase):
    pass


class ProjectUpdate(BaseModel):
    name: str | None = None
    description: str | None = None
    base_url: str | None = None


class ProjectResponse(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
    )

    project_id: uuid.UUID
    user_id: uuid.UUID
    name: str
    description: str | None
    base_url: str
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)




