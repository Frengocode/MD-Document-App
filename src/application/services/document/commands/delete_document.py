from fastapi.encoders import jsonable_encoder

from src.application.core.protocols.service import BaseService
from src.application.core.protocols.verifyer import BaseVerifyer
from src.application.core.repository.document import ABCDocumentRepository
from src.application.services.document.models import Document
from src.application.services.document.scheme import SDocument
from src.application.services.user.scheme import SUser
from src.application.utils.utils import get_logger
import logging


log: logging.Logger = get_logger()



class DeleteDocument(BaseService):
    def __init__(
        self,
        verify_document: BaseVerifyer,
        repository: ABCDocumentRepository
    ) -> None:
        self.verify_document = verify_document
        self.repository = repository



    async def execute(
        self,
        id: int,
        current_user: SUser
    ) -> SDocument:

        # Verify document
        await self.verify_document.verify(id=id, participiant_id=current_user.id)

        deleted_document: Document = await self.repository.delete(id=id)

        log.info("Document successfully deleted | %s", id)

        return SDocument.model_validate(jsonable_encoder(deleted_document))
            