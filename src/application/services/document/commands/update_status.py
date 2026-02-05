from fastapi.encoders import jsonable_encoder

from src.application.core.protocols.service import BaseService
from src.application.core.protocols.verifyer import BaseVerifyer
from src.application.core.repository.document import ABCDocumentRepository
from src.application.services.document.models import Document
from src.application.services.document.scheme import SDocument, SUpdateStatus
from src.application.services.user.exception import RoleException
from src.application.services.user.scheme import Role, SUser


class UpdateStatus(BaseService):
    def __init__(
        self, verify_document: BaseVerifyer, repository: ABCDocumentRepository
    ) -> None:
        self.verify_document = verify_document
        self.repository = repository

    async def execute(self, request: SUpdateStatus, current_user: SUser) -> SDocument:

        if not current_user.role == Role.CHEKER:
            raise RoleException()

        await self.verify_document.verify(
            id=request.id, participiant_id=current_user.id
        )

        updated_document: Document = await self.repository.update_status(
            request=request, id=request.id
        )
        return SDocument.model_validate(jsonable_encoder(updated_document))
