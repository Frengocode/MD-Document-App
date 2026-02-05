from fastapi.encoders import jsonable_encoder
from itertools import zip_longest
from typing import List
from src.application.core.protocols.service import BaseService
from src.application.core.repository.document import ABCDocumentRepository
from src.application.services.document.exception import DocumentNotFoundException
from src.application.services.document.models import Document
from src.application.services.document.scheme import SDocument
from src.application.services.user.scheme import SUser
import asyncio



class GetPariticipantDocuments(BaseService):
    def __init__(
        self,
        repository: ABCDocumentRepository,
        get_user: BaseService
    ) -> None:
        self.repository = repository
        self.get_user = get_user
    

    async def execute(
        self,
        offset: int,
        limit: int,
        current_user: SUser
    ) -> List[SDocument]:
        
        documents: List[Document] = await self.repository.get_all(
            offset=offset,
            limit=limit,
            participiant_id=current_user.id
        )
        if not documents:
            raise DocumentNotFoundException()
        
        users: List[SUser] = await asyncio.gather(
            *[
                self.get_user.execute(
                    user_id=document.user_id
                )
                for document in documents
            ],
            return_exceptions=True
        )

        return [
            SDocument(
                **document.__dict__,
                user=user
            )
            for document, user in zip_longest(documents, users)
        ]
    