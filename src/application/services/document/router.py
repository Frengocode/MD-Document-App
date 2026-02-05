from typing import Annotated, List, BinaryIO
from fastapi.responses import StreamingResponse
from fastapi import APIRouter, Depends, File, UploadFile, Path, Query

from src.application.infrastructure.repository.document import DocumentRepository
from src.application.infrastructure.s3.minio import MinIO
from src.application.infrastructure.verifyer.document.verify_document import (
    VerifyDocument,
)
from src.application.infrastructure.verifyer.document.authors_verifyer import VerifyDocumentAuthors
from src.application.infrastructure.verifyer.user.verifying_of_existing_user import VerifyOfExistingUser
from src.application.services.document.commands.create_document import CreateDocument
from src.application.services.document.commands.update_status import UpdateStatus
from src.application.services.document.dependcies.v1.dependcies import (
    get_document_repository,
    get_minio_s3,
    verify_document,
    verify_authors
)
from src.application.services.document.scheme import SDocument, SUpdateStatus
from src.application.services.user.dependcies.v1.dependcies import (
    get_current_user,
    verify_of_existing_user,
    get_user
)
from src.application.services.user.queries.get_user import GetUser
from src.application.services.user.scheme import SUser
from src.application.services.document.queries.get_document import GetDocument
from src.application.services.document.queries.get_documents import GetDocuments
from src.application.services.document.queries.get_documents_for_user import GetUserDocuments
from src.application.services.document.queries.get_documents_for_participiant import GetPariticipantDocuments
from src.application.services.document.commands.delete_document import DeleteDocument
from src.application.services.document.queries.get_file import GetFile


document_service_router: APIRouter = APIRouter(
    tags=["Document serice"], prefix="/document/service/api/v1"
)


@document_service_router.post("/create/document/", response_model=SDocument)
async def create_document(
    # Fields
    file: Annotated[UploadFile, File(...)],
    participiant_id: int,
    document_name: str,
    # Dependcies
    repository: Annotated[DocumentRepository, Depends(get_document_repository)],
    verify_participiant: Annotated[
        VerifyOfExistingUser, Depends(verify_of_existing_user)
    ],
    minio_s3: Annotated[MinIO, Depends(get_minio_s3)],
    current_user: Annotated[SUser, Depends(get_current_user)],
) -> SDocument:
    service: CreateDocument = CreateDocument(
        repository=repository, verify_participiant=verify_participiant, s3=minio_s3
    )
    return await service.execute(
        file=file,
        participiant_id=participiant_id,
        document_name=document_name,
        current_user=current_user,
    )


@document_service_router.put("/update/status/", response_model=SDocument)
async def update_status(
    repository: Annotated[DocumentRepository, Depends(get_document_repository)],
    verify_document: Annotated[VerifyDocument, Depends(verify_document)],
    request: SUpdateStatus,
    current_user: Annotated[SUser, Depends(get_current_user)],
) -> SDocument:
    service: UpdateStatus = UpdateStatus(
        verify_document=verify_document, repository=repository
    )
    return await service.execute(request=request, current_user=current_user)




@document_service_router.delete(
    "/delete/document/{id}/",
    response_model=SDocument
)
async def delete_document(
    id: Annotated[int, Path(...)],
    repository: Annotated[DocumentRepository, Depends(get_document_repository)],
    current_user: Annotated[SUser, Depends(get_current_user)],
    verify: Annotated[VerifyDocument, Depends(verify_document)]
) -> SDocument:
    service: DeleteDocument = DeleteDocument(verify_document=verify, repository=repository)
    return await service.execute(id=id, current_user=current_user)





@document_service_router.get(
    "/get/documents/for/user/",
    response_model=List[SDocument]
)
async def get_documents_for_user(
    offset: Annotated[int, Query(...)],
    limit: Annotated[int, Query(...)],
    repository: Annotated[DocumentRepository, Depends(get_document_repository)],
    current_user: Annotated[SUser, Depends(get_current_user)]
) -> List[SDocument]:
    service: GetUserDocuments = GetUserDocuments(repository=repository)
    return await service.execute(offset=offset, limit=limit, current_user=current_user)




@document_service_router.get(
    "/get/documents/for/participiant/",
    response_model=List[SDocument]
)
async def get_documents_for_participant(
    offset: Annotated[int, Query(...)],
    limit: Annotated[int, Query(...)],
    repository: Annotated[DocumentRepository, Depends(get_document_repository)],
    current_user: Annotated[SUser, Depends(get_current_user)],
    get_user: Annotated[GetUser, Depends(get_user)]
) -> List[SDocument]:
    service: GetPariticipantDocuments = GetPariticipantDocuments(repository=repository, get_user=get_user)
    return await service.execute(offset=offset, limit=limit, current_user=current_user)




@document_service_router.get(
    "/get/document/{id}/",
    response_model=SDocument
)
async def get_document(
    id: Annotated[int, Path(...)],
    current_user: Annotated[SUser, Depends(get_current_user)],
    verify_authors: Annotated[VerifyDocumentAuthors, Depends(verify_authors)],
    repository: Annotated[DocumentRepository, Depends(get_document_repository)],
    get_user: Annotated[GetUser, Depends(get_user)]
) -> SDocument:
    service: GetDocument = GetDocument(repository=repository, verify_authors=verify_authors, get_user=get_user)
    return await service.execute(id=id, current_user=current_user)



@document_service_router.get(
    "/get/document/file/",
)
async def get_document_file(
    filename: Annotated[str, Query(...)],
    minio: Annotated[MinIO, Depends(get_minio_s3)]  
) -> StreamingResponse:
    service: GetFile = GetFile(s3=minio)
    file: BinaryIO = await service.execute(filename=filename)
    
    return StreamingResponse(
        file,
        media_type="application/octet-stream",
        headers={
            "Content-Disposition": f'attachment; filename="{filename}"'
        }
    )



@document_service_router.get(
    "/get/documents/",
    response_model=List[SDocument]
)
async def get_documents(
    offset: Annotated[int, Query(...)],
    limit: Annotated[int, Query(...)],
    repository: Annotated[DocumentRepository, Depends(get_document_repository)],
    get_user: Annotated[GetUser, Depends(get_user)]
) -> List[SDocument]:
    service: GetDocuments = GetDocuments(repository=repository, get_user=get_user)
    return await service.execute(offset=offset, limit=limit)

