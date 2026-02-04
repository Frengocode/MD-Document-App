from typing import BinaryIO, Protocol, Type

from fastapi import UploadFile


class S3(Protocol):

    async def put(self, bucket_name: str, file: Type[UploadFile]) -> str: ...

    async def get(self, bucket_name: str, filename: str) -> BinaryIO | None: ...
