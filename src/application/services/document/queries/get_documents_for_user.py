from fastapi.encoders import jsonable_encoder
from typing import List
from src.application.core.protocols.service import BaseService
from src.application.core.repository.document import ABCDocumentRepository
from src.application.services.document.exception import DocumentNotFoundException
from src.application.services.document.models import Document
from src.application.services.document.scheme import SDocument
from src.application.services.user.scheme import SUser




class GetUserDocuments(BaseService):
    def __init__(
        self,
        repository: ABCDocumentRepository
    ) -> None:
        self.repository = repository
    

    async def execute(
        self,
        offset: int,
        limit: int,
        current_user: SUser
    ) -> List[SDocument]:
        
        documents: List[Document] = await self.repository.get_all(
            offset=offset,
            limit=limit,
            user_id=current_user.id
        )
        if not documents:
            raise DocumentNotFoundException()
        

        return [
            SDocument.model_validate(
                jsonable_encoder(document)
            )
            for document in documents
        ]
    