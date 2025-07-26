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


class DocBase(BaseModel):
    name: constr(max_length=255)
    type: DocType
    format: DocFormat
    status: DocStatus = DocStatus.PENDING


class DocCreate(DocBase):
    pass


class DocResponse(DocBase):
    id: UUID
    presigned_url: HttpUrl


class DocUpdateStatus(BaseModel):
    status: DocStatus
