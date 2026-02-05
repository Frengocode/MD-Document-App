from typing import Annotated

from fastapi import Depends
from minio import Minio
from sqlalchemy.ext.asyncio import AsyncSession

from src.application.core.config.config import settings
from src.application.core.database.database import get_session
from src.application.infrastructure.repository.document import DocumentRepository
from src.application.infrastructure.s3.minio import MinIO
from src.application.infrastructure.verifyer.document.verify_document import (
    VerifyDocument
)
from src.application.infrastructure.verifyer.document.authors_verifyer import VerifyDocumentAuthors



async def get_minio_s3() -> MinIO: 
    client: Minio = Minio(
        endpoint=settings.MINIO.MINIO_HOST,
        access_key=settings.MINIO.MINIO_USERNAME,
        secret_key=settings.MINIO.MINIO_PASSWORD,
        secure=False,
    )
    return MinIO(client=client)


async def get_document_repository(
    session: Annotated[AsyncSession, Depends(get_session)],
) -> DocumentRepository:
    return DocumentRepository(session=session)


async def verify_document(
    repository: Annotated[DocumentRepository, Depends(get_document_repository)],
) -> VerifyDocument:
    return VerifyDocument(repository=repository)



async def verify_authors(
    repository: Annotated[DocumentRepository, Depends(get_document_repository)]
) -> VerifyDocumentAuthors:
    return VerifyDocumentAuthors(repository=repository)


