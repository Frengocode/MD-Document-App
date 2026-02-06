import asyncio

from fastapi.encoders import jsonable_encoder

from src.application.core.protocols.service import BaseService
from src.application.core.protocols.verifyer import BaseVerifyer
from src.application.core.repository.document import ABCDocumentRepository
from src.application.services.document.models import Document
from src.application.services.document.scheme import SDocument
from src.application.services.user.scheme import SUser


class GetDocument(BaseService):
    def __init__(
        self,
        repository: ABCDocumentRepository,
        verify_authors: BaseVerifyer,
        get_user: BaseService,
    ) -> None:
        self.repository = repository
        self.verify_authors = verify_authors
        self.get_user = get_user

    async def execute(self, id: int, current_user: SUser) -> SDocument:

        await self.verify_authors.verify(id=id, current_user_id=current_user.id)

        document: Document = await self.repository.get(id=id)

        user: SUser = await asyncio.gather(
            self.get_user.execute(user_id=document.user_id), return_exceptions=True
        )
        return SDocument(**jsonable_encoder(document), user=user[0])
