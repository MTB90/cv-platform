import logging
from typing import Optional
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

from core.exceptions import ConflictError
from domain.doc import Doc
from infra.models import DocModel
from infra.repo.base import BaseRepository

logger = logging.getLogger(__name__)


class DocRepository(BaseRepository):
    async def get_by_id(self, doc_id: UUID) -> Optional[Doc]:
        result = await self.db.execute(select(DocModel).where(DocModel.id == doc_id))
        doc_record = result.scalar_one_or_none()

        if doc_record is None:
            return None

        return Doc(**doc_record.__dict__)

    async def create(self, doc: Doc) -> Doc:
        doc_record = DocModel(**doc.__dict__)

        try:
            await self.add_and_commit(doc_record)
        except IntegrityError:
            raise ConflictError("Doc Creation Failed")

        await self.db.refresh(doc_record)

        doc.created_at = doc_record.created_at
        return doc
