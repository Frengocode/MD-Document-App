from src.application.core.protocols.verifyer import BaseVerifyer
from src.application.core.repository.document import ABCDocumentRepository
from src.application.services.document.exception import DocumentNotFoundException


class VerifyDocumentAuthors(BaseVerifyer):
    def __init__(self, repository: ABCDocumentRepository) -> None:
        self.repository = repository

    async def verify(self, id: int, current_user_id: int) -> None:
        doc = await self.repository.get(id=id, user_id=current_user_id)

        if not doc:
            doc = await self.repository.get(id=id, participiant_id=current_user_id)

        if not doc:
            raise DocumentNotFoundException()
