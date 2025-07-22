from datetime import datetime

from sqlmodel import SQLModel


class UserBase(SQLModel):
    name: str
    email: str


class UserCreate(UserBase):
    pass


class UserResponse(UserBase):
    created_at: datetime
