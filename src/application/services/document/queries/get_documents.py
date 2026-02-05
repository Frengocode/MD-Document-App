from itertools import zip_longest
from src.application.core.repository.document import ABCDocumentRepository
from src.application.services.document.scheme import SDocument
from src.application.core.protocols.service import BaseService
from src.application.services.document.models import Document
from src.application.services.user.scheme import SUser
from typing import List
import asyncio






class GetDocuments(BaseService):
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
        limit: int
    ) -> List[SDocument]:
    
        documents: List[Document] = await self.repository.get_all(
            offset=offset,
            limit=limit
        )
        
        users: List[SUser] = await asyncio.gather(
            *[
                self.get_user.execute(
                    document.user_id
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
    