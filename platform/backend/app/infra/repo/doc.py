import logging
from typing import Optional
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

from core.exceptions import ConflictError
from domain.doc import Doc
from infra.mapper import DocMapper
from infra.models import DocModel
from infra.repo.base import BaseRepository

logger = logging.getLogger(__name__)


class DocRepository(BaseRepository):
    async def get_by_id(self, db_session, doc_id: UUID) -> Optional[Doc]:
        result = await db_session.execute(select(DocModel).where(DocModel.id == doc_id))
        doc_record = result.scalar_one_or_none()

        if doc_record is None:
            return None

        return DocMapper.to_domain(doc_record)

    async def create(self, db_session, doc: Doc) -> Doc:
        doc_record = DocMapper.from_domain(doc)

        try:
            await self.add_and_commit(db_session, doc_record)
        except IntegrityError:
            raise ConflictError("Doc Creation Failed")

        return doc
