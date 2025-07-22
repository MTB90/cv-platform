from models import Doc, User
from repository.base import BaseRepository
from schema.doc import DocBase


class DocRepository(BaseRepository):
    async def create(self, user: User, doc_data: DocBase) -> Doc:
        doc = Doc(name=doc_data.name, type=doc_data.type, user_id=user.id)

        self.db.add(doc)
        await self.db.commit()
        await self.db.refresh(doc)
        return doc
