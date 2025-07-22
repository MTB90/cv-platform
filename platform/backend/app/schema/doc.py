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


class CVCreate(DocBase):
    type: DocType = DocType.CV


class CVResponse(DocBase):
    id: UUID
    type: DocType = DocType.CV
    format: DocFormat
    presigned_url: HttpUrl
