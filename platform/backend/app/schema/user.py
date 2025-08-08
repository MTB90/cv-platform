from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, constr


class User(BaseModel):
    id: UUID
    name: constr(max_length=255)
    email: constr(max_length=255)


class UserCreate(BaseModel):
    name: constr(max_length=255)
    email: constr(max_length=255)


class UserResponse(BaseModel):
    id: UUID
    name: constr(max_length=255)
    email: constr(max_length=255)
    created_at: datetime
