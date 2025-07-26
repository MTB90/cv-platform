import logging
from typing import Optional
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

from core.exceptions import DocIntegrityError
from models import Doc
from repository.base import BaseRepository
from schema.doc import DocBase

logger = logging.getLogger(__name__)


class DocRepository(BaseRepository):
    async def get_by_id(self, doc_id: UUID) -> Optional[Doc]:
        result = await self.db.execute(select(Doc).where(Doc.id == doc_id))
        return result.scalar_one_or_none()

    async def create(self, id: UUID, user_id: UUID, data: DocBase) -> Doc:
        doc = Doc(**data.__dict__, id=id, user_id=user_id)

        try:
            await self.add_and_commit(doc)
        except IntegrityError:
            logger.error("doc creation failed", extra={"doc": doc.id})
            raise DocIntegrityError()

        await self.db.refresh(doc)
        return doc
