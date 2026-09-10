from __future__ import annotations
from datetime import datetime
import uuid
from pydantic import BaseModel, ConfigDict, EmailStr
from pydantic import BaseModel


class EndpointBase(BaseModel):
    method: str
    path: str
    summary: str | None = None
    description: str | None = None
    request_body: str | None = None
    response_body: str | None = None
    response_status_code: int | None = None

class EndpointCreate(EndpointBase):
    pass


class EndpointUpdate(BaseModel):
    method: str | None = None
    path: str | None = None
    summary: str | None = None
    description: str | None = None
    request_body: str | None = None
    response_body: str | None = None
    response_status_code: int | None = None

class EndpointResponse(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
    )

    endpoint_id: uuid.UUID
    project_id: uuid.UUID
    method: str
    path: str
    summary: str | None
    description: str | None
    request_body: str | None
    response_body: str | None
    response_status_code: int | None
    created_at: datetime
    updated_at: datetime