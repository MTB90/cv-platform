from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from uuid import UUID


class JobType(str, Enum):
    FORMATING = "formating"


class JobStatus(str, Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"


@dataclass
class Job:
    id: UUID
    type: JobType
    status: JobStatus
    source_id: UUID
    result_id: UUID
    created_at: datetime
    updated_at: datetime
