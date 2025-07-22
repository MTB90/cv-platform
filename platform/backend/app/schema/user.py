from datetime import datetime
from typing import Optional
from uuid import UUID

from sqlmodel import SQLModel


class UserBase(SQLModel):
    name: str
    email: str


class UserCreate(UserBase):
    pass


class UserResponse(UserBase):
    created_at: datetime

