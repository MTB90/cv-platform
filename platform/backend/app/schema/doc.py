from uuid import UUID

from sqlmodel import SQLModel


class DocBase(SQLModel):
    name: str
    type: str


class CreateCV(DocBase):
    type: str = "CV"


class CrateCVResponse(DocBase):
    id: UUID
    type: str = "CV"
    presigned_url: str
