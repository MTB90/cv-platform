from enum import Enum
from uuid import UUID

from pydantic import HttpUrl
from sqlmodel import SQLModel


class DocType(Enum):
    CV = "CV"


class DocFormat(Enum):
    PDF = "pdf"
    TXT = "txt"


class DocBase(SQLModel):
    name: str
    type: DocType
    format: DocFormat


class CreateCV(DocBase):
    type: DocType = DocType.CV


class CreateCVResponse(DocBase):
    id: UUID
    type: DocType = DocType.CV
    presigned_url: HttpUrl
