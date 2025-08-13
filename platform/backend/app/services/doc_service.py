import datetime
import logging
from uuid import UUID, uuid4

from core.exceptions import UserNotFoundError, DocNotFoundError
from domain.doc import Doc, DocStatus
from infra.repo.doc import DocRepository
from infra.repo.user import UserRepository
from schema.doc import DocCreate, DocEvent, DocPresignedUrl, DocResponse
from utils.storage import StorageClient

logger = logging.getLogger(__name__)


class DocService:
    def __init__(self, storage: StorageClient, user_repo: UserRepository, doc_repo: DocRepository):
        self._storage = storage
        self._user_repo = user_repo
        self._doc_repo = doc_repo

    async def list_docs(self, user_id: UUID):
        logger.info(f"list docs for user: {user_id}")
        docs = await self._doc_repo.get_all()
        return [DocResponse(**doc.__dict__) for doc in docs]

    async def create_doc(self, user_id: UUID, data: DocCreate) -> DocPresignedUrl:
        logger.info("creating doc", extra={"user_id": user_id, "data": data})

        user = await self._user_repo.get_by_id(user_id)
        if user is None:
            raise UserNotFoundError(user_id)

        doc_id = uuid4()
        object_name = f"{user_id}/{doc_id}.{data.format.value}"

        logger.info("get presigned url for upload")
        presigned_url = await self._storage.presigned_put_object(object_name)

        doc_create = Doc(
            id=doc_id,
            user_id=user_id,
            name=data.name,
            type=data.type,
            format=data.format,
            status=DocStatus.UPLOADING,
            created_at=datetime.datetime.now(datetime.UTC),
            updated_at=datetime.datetime.now(datetime.UTC),
        )

        doc = await self._doc_repo.create(doc_create)
        logger.info("doc created", extra={"doc": doc})

        return DocPresignedUrl(presigned_url=presigned_url)

    async def update_doc_status(self, data: DocEvent):
        logger.info("updating doc status", extra={"data": data})

        user = await self._user_repo.get_by_id(data.user_id)
        if user is None:
            raise UserNotFoundError(data.user_id)

        updated_at = datetime.datetime.now(datetime.UTC)
        doc = await self._doc_repo.update_status(data.doc_id, DocStatus(data.status), updated_at)
        if doc is None:
            raise DocNotFoundError(data.doc_id)

        logger.info("doc updated", extra={"doc": doc})
