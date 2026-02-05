from typing import Type

from fastapi import UploadFile
from fastapi.encoders import jsonable_encoder

from src.application.core.constants.constants import constants
from src.application.core.protocols.s3 import S3
from src.application.core.protocols.service import BaseService
from src.application.core.protocols.verifyer import BaseVerifyer
from src.application.core.repository.document import ABCDocumentRepository
from src.application.services.document.models import Document
from src.application.services.document.scheme import SDocument
from src.application.services.user.scheme import SUser


class CreateDocument(BaseService):
    def __init__(
        self,
        repository: ABCDocumentRepository,
        verify_participiant: BaseVerifyer,
        s3: S3,
    ) -> None:
        self.repository = repository
        self.verify_participiant = verify_participiant
        self.s3 = s3

    async def execute(
        self,
        file: Type[UploadFile],
        participiant_id: int,
        document_name: str,
        current_user: SUser,
    ) -> SDocument:

        # Verifyes paritcipiant existing
        await self.verify_participiant.verify(id=participiant_id)

        # Saving file into S3
        saved_file: str = await self.s3.put(
            bucket_name=constants.BUCKETS.DOCUMENTS_BUCKET, file=file
        )

        # Saving document into db
        document: Document = await self.repository.put_document(
            filename=saved_file,
            file_url=f"{constants.URLS.GET_DOCUMENT_URL}/{saved_file}",
            document_name=document_name,
            user_id=current_user.id,
            participiant_id=participiant_id,
        )

        return SDocument.model_validate(jsonable_encoder(document))
