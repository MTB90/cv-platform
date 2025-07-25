from uuid import UUID

from models import Doc
from repository.base import BaseRepository
from schema.doc import DocBase


class DocRepository(BaseRepository):
    async def create(self, id: UUID, user_id: UUID, data: DocBase) -> Doc:
        doc = Doc(**data.__dict__, id=id, user_id=user_id)

        await self.add_and_commit(doc)
        await self.db.refresh(doc)
        return doc
