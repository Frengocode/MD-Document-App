import io
import logging
import os
import uuid
from typing import BinaryIO
from fastapi import UploadFile
from minio import Minio, S3Error

from src.application.core.protocols.s3 import S3
from src.application.services.document.exception import SaveDocumentException, DocumentNotFoundException
from src.application.utils.utils import get_logger

log: logging.Logger = get_logger()


class MinIO(S3):
    def __init__(self, client: Minio) -> None:
        self.client = client

    async def put(self, bucket_name: str, file: UploadFile) -> str:
        try:
            # Read file content
            content = await file.read()

            # Convert bytes to a file-like object
            file_stream = io.BytesIO(content)

            # Generate unique filename
            ext = os.path.splitext(file.filename)[1]
            unique_id = uuid.uuid4().hex
            unique_filename = f"{unique_id}{ext}"

            # Save to bucket
            self.client.put_object(
                bucket_name=bucket_name,
                object_name=unique_filename,
                data=file_stream,  
                length=len(content),
                content_type=file.content_type,  
            )

            log.info("File successfully saved into bucket | %s", bucket_name)
            return unique_filename

        except Exception:
            log.error("Can't save file into bucket | %s", bucket_name, exc_info=True)
            raise SaveDocumentException()




    async def get(
        self,
        bucket_name: str,
        filename: str
    ) -> BinaryIO:
        try:
            response = self.client.get_object(
                bucket_name=bucket_name,
                object_name=filename
            )

            return response

        except S3Error:
            log.error(
                "Can't get file %s from bucket %s",
                filename,
                bucket_name,
                exc_info=True
            )
            raise DocumentNotFoundException()