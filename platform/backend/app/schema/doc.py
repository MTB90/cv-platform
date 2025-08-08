from typing import Any
from uuid import UUID

from pydantic import HttpUrl, BaseModel, constr, model_validator, Field, field_validator
from pydantic_core import PydanticCustomError, InitErrorDetails, ValidationError

from domain.doc import DocType, DocFormat, DocStatus


class DocCreate(BaseModel):
    name: constr(max_length=255)
    type: DocType
    format: DocFormat


class DocResponse(BaseModel):
    id: UUID
    name: constr(max_length=255)
    type: DocType
    format: DocFormat
    status: DocStatus
    presigned_url: HttpUrl


class DocEventStatus(BaseModel):
    user_id: UUID
    doc_id: UUID

    key: str = Field(alias="Key")
    event_name: str = Field(alias="EventName")

    @field_validator("event_name", mode="after")
    @classmethod
    def validate_event(cls, value: str) -> str:
        if value in ["s3:ObjectCreated:Post", "s3:ObjectCreated:Put"]:
            return DocStatus.READY

        if value == "s3:ObjectRemoved:Delete":
            return DocStatus.DELETED

        raise ValueError("unsupported event")

    @model_validator(mode="before")
    @classmethod
    def validate_key(cls, data: Any) -> Any:
        if isinstance(data, dict):
            if data.get("user_id") and data.get("doc_id"):
                return data

            key = data.get("Key")
            if key is None:
                validation_errors = [
                    InitErrorDetails(
                        type=PydanticCustomError("missing", "Field required"),
                        loc=("Key",),
                        input=data,
                        ctx={},
                    )
                ]
                raise ValidationError.from_exception_data(
                    title=cls.__class__.__name__, line_errors=validation_errors
                )

            key_split = key.split("/")
            if len(key_split) != 3:
                raise ValueError("can't find user_id and doc_id in Key")

            data["user_id"] = key_split[1]
            data["doc_id"] = key_split[2].split(".")[0]

        return data
