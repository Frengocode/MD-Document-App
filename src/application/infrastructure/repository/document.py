from dataclasses import dataclass
from typing import Any, List

from sqlalchemy import Result, Select, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.application.core.repository.document import ABCDocumentRepository
from src.application.services.document.models import Document
from src.application.services.document.scheme import SUpdateStatus


@dataclass
class DocumentRepository(ABCDocumentRepository):
    session: AsyncSession
    model = Document

    async def put_document(
        self,
        filename: str,
        file_url: str,
        user_id: int,
        participiant_id: int,
        document_name: str,
    ) -> Document:
        document: Document = Document(
            filename=filename,
            document_url=file_url,
            user_id=user_id,
            document_name=document_name,
            participiant_id=participiant_id,
        )
        self.session.add(document)
        await self.session.commit()
        await self.session.refresh(document)
        return document

    async def get_all(self, offset: int, limit: int, **filters: Any) -> List[Document]:
        stmt: Select[Document] = (
            select(self.model)
            .offset(offset)
            .limit(limit)
            .filter_by(**filters)
            .order_by(self.model.created_at.desc())
        )
        result: Result[Document] = await self.session.execute(stmt)
        return result.scalars().all()

    async def update_status(self, request: SUpdateStatus, **filters: Any) -> Document:
        stmt: Select[Document] = select(self.model).filter_by(**filters)
        result: Result[Document] = await self.session.execute(stmt)
        document: Document = result.scalars().first()

        for name, value in request.model_dump().items():
            setattr(document, name, value)
        await self.session.commit()
        await self.session.refresh(document)
        return document

    async def delete(self, **filters: Any) -> Document:
        stmt: Select[Document] = select(self.model).filter_by(**filters)
        result: Result[Document] = await self.session.execute(stmt)
        document: Document = result.scalars().first()
        await self.session.delete(document)
        await self.session.commit()
        return document

    async def get(self, **filters: Any) -> Document | None:
        stmt: Select[Document] = select(self.model).filter_by(**filters)
        result: Result[Document] = await self.session.execute(stmt)
        return result.scalars().first()
