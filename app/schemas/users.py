
from __future__ import annotations
from datetime import datetime
import uuid
from pydantic import BaseModel, ConfigDict, EmailStr


class UserBase(BaseModel):
    email: EmailStr
    password: str

class UserCreate(UserBase):
    pass

class UserResponse(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
    )

    user_id: uuid.UUID
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
    )

    user_id: uuid.UUID
    email: EmailStr
    created_at: datetime


class TokenResponse(BaseModel):
    access_token: str
    token_type: str

