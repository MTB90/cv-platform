import logging
from uuid import UUID, uuid4

from sqlmodel.ext.asyncio.session import AsyncSession

from core.exceptions import UserNotFoundError
from repository.doc import DocRepository
from repository.user import UserRepository
from schema.doc import DocCreate, CVResponse
from utils.storage import MinioClient

logger = logging.getLogger(__name__)


class DocService:
    def __init__(self, db: AsyncSession, storage: MinioClient):
        self._db = db
        self._storage = storage
        self._user_repo = UserRepository(db)
        self._doc_repo = DocRepository(db)

    async def create_cv(self, user_id: UUID, doc_data: DocCreate) -> CVResponse:
        logger.info("creating new doc", extra={"user": user_id, "doc": doc_data})

        user = await self._user_repo.get_by_id(user_id)
        if user is None:
            raise UserNotFoundError()

        doc_id = uuid4()
        object_name = f"{user_id}/{doc_id}.{doc_data.format}"

        logger.info("get presigned url for upload")
        presigned_url = await self._storage.presigned_put_object(object_name)
        doc = await self._doc_repo.create(doc_id, user_id, doc_data)
        logger.info("doc created", extra={"doc": doc})

        return CVResponse(**doc.__dict__, presigned_url=presigned_url)
