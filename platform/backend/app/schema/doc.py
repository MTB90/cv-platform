from sqlmodel import SQLModel


class DocBase(SQLModel):
    name: str
    type: str


class CreateCV(DocBase):
    type: str = "CV"
