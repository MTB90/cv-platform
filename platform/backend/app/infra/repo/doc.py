import logging
from typing import Optional
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

from core.exceptions import ConflictError
from infra.repo.base import BaseRepository
from infra.models import DocModel
from schema.doc import DocCreate

logger = logging.getLogger(__name__)


class DocRepository(BaseRepository):
    async def get_by_id(self, doc_id: UUID) -> Optional[DocModel]:
        result = await self.db.execute(select(DocModel).where(DocModel.id == doc_id))
        return result.scalar_one_or_none()

    async def create(self, user_id: UUID, id: UUID, data: DocCreate) -> DocModel:
        doc = DocModel(**data.__dict__, id=id, user_id=user_id)

        try:
            await self.add_and_commit(doc)
        except IntegrityError:
            raise ConflictError("Doc Creation Failed")

        await self.db.refresh(doc)
        return doc
