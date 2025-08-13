import logging
from datetime import datetime
from typing import Optional, Sequence
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

from core.exceptions import ConflictError
from domain.doc import Doc, DocStatus
from infra.mapper import DocMapper
from infra.models import DocModel
from infra.repo.base import BaseRepository

logger = logging.getLogger(__name__)


class DocRepository(BaseRepository):
    async def get_all(self, user_id: UUID) -> Sequence[Doc]:
        result = await self.db.execute(select(DocModel).where(DocModel.user_id == user_id))
        doc_records = result.scalars().all()

        return [DocMapper.to_domain(doc_record) for doc_record in doc_records]

    async def get_by_id(self, doc_id: UUID) -> Optional[Doc]:
        result = await self.db.execute(select(DocModel).where(DocModel.id == doc_id))
        doc_record = result.scalar_one_or_none()

        if doc_record is None:
            return None

        return DocMapper.to_domain(doc_record)

    async def create(self, doc: Doc) -> Doc:
        doc_record = DocMapper.from_domain(doc)

        try:
            await self.add_and_commit(doc_record)
        except IntegrityError:
            raise ConflictError("Doc Creation Failed")

        return doc

    async def update_status(
        self, doc_id: UUID, status: DocStatus, updated_at: datetime
    ) -> Optional[Doc]:
        result = await self.db.execute(select(DocModel).where(DocModel.id == doc_id))
        doc_record: DocModel = result.scalar_one_or_none()

        doc_record.status = status
        doc_record.updated_at = updated_at

        try:
            await self.add_and_commit(doc_record)
            return DocMapper.to_domain(doc_record)
        except IntegrityError:
            raise ConflictError("Doc Update Failed")
