from datetime import datetime
from uuid import UUID, uuid4

from sqlmodel import Column, DateTime, func
from sqlmodel import SQLModel, Field


class UserBase(SQLModel):
    name: str
    email: str


class User(UserBase, table=True):
    __tablename__ = 'users'

    id: UUID = Field(default_factory=uuid4, nullable=False, primary_key=True)
    created_at: datetime = Field(
        sa_column=Column(DateTime(), server_default=func.now(), nullable=False)
    )


class UserCreate(UserBase):
    pass
