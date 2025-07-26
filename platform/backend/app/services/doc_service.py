import logging
from uuid import UUID, uuid4

from sqlmodel.ext.asyncio.session import AsyncSession

from core.exceptions import UserNotFoundError, DocNotFoundError
from repository.doc import DocRepository
from repository.user import UserRepository
from schema.doc import DocCreate, DocUpdateStatus, DocResponse
from utils.storage import MinioClient

logger = logging.getLogger(__name__)


class DocService:
    def __init__(self, db: AsyncSession, storage: MinioClient):
        self._db = db
        self._storage = storage
        self._user_repo = UserRepository(db)
        self._doc_repo = DocRepository(db)

    async def create(self, user_id: UUID, data: DocCreate) -> DocResponse:
        logger.info("creating doc", extra={"user": user_id, "data": data})

        user = await self._user_repo.get_by_id(user_id)
        if user is None:
            raise UserNotFoundError()

        doc_id = uuid4()
        object_name = f"{user_id}/{doc_id}.{data.format}"

        logger.info("get presigned url for upload")
        presigned_url = await self._storage.presigned_put_object(object_name)
        doc = await self._doc_repo.create(doc_id, user_id, data)
        logger.info("doc created", extra={"doc": doc})

        return DocResponse(**doc.__dict__, presigned_url=presigned_url)

    async def update_status(self, doc_id: UUID, data: DocUpdateStatus):
        logger.info("updating doc status", extra={"id": doc_id, "data": data})

        doc = await self._doc_repo.get_by_id(doc_id)
        if doc is None:
            raise DocNotFoundError()

        doc.status = data.status
        await self._doc_repo.add_and_commit(doc)

        logger.info("doc updated", extra={"doc": doc})
