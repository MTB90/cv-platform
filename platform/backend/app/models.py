from datetime import datetime
from typing import Optional
from uuid import UUID, uuid4

from sqlalchemy import Column, DateTime, func, String
from sqlmodel import Field, SQLModel

from schema.doc import DocType, DocFormat, DocStatus


class Doc(SQLModel, table=True):
    __tablename__ = "docs"

    id: Optional[UUID] = Field(default_factory=uuid4, primary_key=True)
    user_id: UUID = Field(default=None, nullable=False, foreign_key="users.id")
    name: str = Field(sa_column=Column(String(255), nullable=False))
    type: str = Field(sa_column=Column(String(50), nullable=False))
    format: str = Field(sa_column=Column(String(50), nullable=False))
    status: str = Field(
        sa_column=Column(String(50), nullable=False, default=DocStatus.PENDING.value)
    )

    created_at: datetime = Field(
        sa_column=Column(DateTime(), server_default=func.now(), nullable=False)
    )
    updated_at: Optional[datetime] = Field(
        sa_column=Column(DateTime(), server_default=func.now(), nullable=False)
    )


class User(SQLModel, table=True):
    __tablename__ = "users"

    id: UUID = Field(default_factory=uuid4, nullable=False, primary_key=True)
    name: str = Field(sa_column=Column(String(255), nullable=False))
    email: str = Field(sa_column=Column(String(255), nullable=False, unique=True))
    created_at: datetime = Field(
        sa_column=Column(DateTime(), server_default=func.now(), nullable=False)
    )
