from datetime import datetime
from sqlmodel import Column, DateTime, func
from sqlmodel import SQLModel, Field
from typing import Optional
from uuid import UUID, uuid4


class DocBase(SQLModel):
    name: str
    type: str


class Doc(SQLModel, table=True):
    __tablename__ = 'docs'

    id: Optional[UUID] = Field(default_factory=uuid4, primary_key=True)
    user_id: UUID = Field(default=None, nullable=False, foreign_key="users.id")

    created_at: datetime = Field(
        sa_column=Column(DateTime(), server_default=func.now(), nullable=False)
    )
    updated_at: Optional[datetime] = Field(
        sa_column=Column(DateTime(), server_default=func.now(), nullable=False)
    )


class DocCreate(DocBase):
    pass
