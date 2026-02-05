from src.application.core.protocols.s3 import S3
from src.application.core.protocols.service import BaseService
from src.application.core.constants.constants import constants
from typing import BinaryIO




class GetFile(BaseService):
    def __init__(
        self,
        s3: S3
    ) -> None:
        self.s3 = s3

    
    async def execute(
        self,
        filename: str
    ) -> BinaryIO:
        return await self.s3.get(bucket_name=constants.BUCKETS.DOCUMENTS_BUCKET, filename=filename)
