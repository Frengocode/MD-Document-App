from src.application.core.protocols.verifyer import BaseVerifyer
from src.application.core.repository.document import ABCDocumentRepository
from src.application.services.document.exception import DocumentNotFoundException
from src.application.services.document.models import Document


class VerifyDocument(BaseVerifyer):
    def __init__(self, repository: ABCDocumentRepository) -> None:
        self.repository = repository

    async def verify(self, id: int, participiant_id: int) -> Document:
        document: Document | None = await self.repository.get(
            id=id, participiant_id=participiant_id
        )
        if not document:
            raise DocumentNotFoundException()
