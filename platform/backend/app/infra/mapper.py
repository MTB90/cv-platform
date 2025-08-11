from dataclasses import asdict

from domain.doc import Doc
from domain.job import Job
from domain.user import User
from infra.models import UserModel, DocModel, JobModel


class UserMapper:
    @staticmethod
    def to_domain(model: UserModel) -> User:
        return User(**model.model_dump())

    @staticmethod
    def from_domain(user: User) -> UserModel:
        return UserModel(**asdict(user))


class DocMapper:
    @staticmethod
    def to_domain(model: DocModel) -> Doc:
        return Doc(**model.model_dump())

    @staticmethod
    def from_domain(doc: Doc) -> DocModel:
        return DocModel(**asdict(doc))


class JobMapper:
    @staticmethod
    def to_domain(model: JobModel) -> Job:
        return Job(**model.model_dump())

    @staticmethod
    def from_domain(job: Job) -> JobModel:
        return JobModel(**asdict(job))
