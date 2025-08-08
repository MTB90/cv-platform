from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from uuid import UUID


class DocType(str, Enum):
    CV = "CV"


class DocFormat(str, Enum):
    PDF = "pdf"
    TXT = "txt"


class DocStatus(str, Enum):
    UPLOADING = "uploading"
    PROCESSING = "processing"
    DELETED = "deleted"
    FAILED = "failed"
    READY = "ready"


@dataclass
class Doc:
    id: UUID
    user_id: UUID
    name: str
    type: DocType
    status: DocStatus
    format: DocFormat
    created_at: datetime = None
    updated_at: datetime = None
