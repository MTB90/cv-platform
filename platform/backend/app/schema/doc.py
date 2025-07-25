from enum import Enum
from uuid import UUID

from pydantic import HttpUrl, BaseModel, constr


class DocType(str, Enum):
    CV = "CV"


class DocFormat(str, Enum):
    PDF = "pdf"
    TXT = "txt"


class DocStatus(str, Enum):
    PENDING = "pending"
    UPLOADED = "uploaded"
    DELETED = "deleted"


class DocBase(BaseModel):
    name: constr(max_length=255)
    type: DocType
    format: DocFormat
    status: DocStatus = DocStatus.PENDING


class DocUpdateStatus(BaseModel):
    status: DocStatus


class CVCreate(DocBase):
    type: DocType = DocType.CV


class CVResponse(DocBase):
    id: UUID
    type: DocType = DocType.CV
    presigned_url: HttpUrl
