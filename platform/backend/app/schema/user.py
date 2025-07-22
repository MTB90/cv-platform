from datetime import datetime
from uuid import UUID

from sqlmodel import SQLModel


class UserBase(SQLModel):
    name: str
    email: str


class UserCreate(UserBase):
    pass


class UserResponse(UserBase):
    id: UUID
    created_at: datetime
