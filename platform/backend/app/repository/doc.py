from repository.base import BaseRepository
from schema.doc import Doc, DocCreate
from schema.user import User


class DocRepository(BaseRepository):
    async def create(self, user: User, doc_data: DocCreate) -> Doc:
        doc = Doc(
            name=doc_data.name,
            type=doc_data.type,
            user_id=user.id
        )
        self.db_session.add(doc)
        await self.db_session.commit()
        await self.db_session.refresh(doc)
        return doc
