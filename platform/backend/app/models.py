from datetime import datetime
from typing import Optional
from uuid import UUID, uuid4

from sqlalchemy import Column, DateTime, func
from sqlmodel import Field

from schema.doc import DocBase
from schema.user import UserBase


class Doc(DocBase, table=True):
    __tablename__ = 'docs'

    id: Optional[UUID] = Field(default_factory=uuid4, primary_key=True)
    user_id: UUID = Field(default=None, nullable=False, foreign_key="users.id")

    created_at: datetime = Field(
        sa_column=Column(DateTime(), server_default=func.now(), nullable=False)
    )
    updated_at: Optional[datetime] = Field(
        sa_column=Column(DateTime(), server_default=func.now(), nullable=False)
    )


class User(UserBase, table=True):
    __tablename__ = 'users'

    id: UUID = Field(default_factory=uuid4, nullable=False, primary_key=True)
    created_at: datetime = Field(
        sa_column=Column(DateTime(), server_default=func.now(), nullable=False)
    )
