from models import Doc, User
from repository.base import BaseRepository
from schema.doc import DocBase


class DocRepository(BaseRepository):
    async def create(self, user: User, data: DocBase) -> Doc:
        doc = Doc(**data.__dict__, user_id=user.id)

        await self.add_and_commit(doc)
        await self.db.refresh(doc)
        return doc
