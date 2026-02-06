from abc import ABC, abstractmethod
from typing import Any, List, Type, TypeVar

from pydantic import BaseModel

T = TypeVar("T")


class ABCDocumentRepository(ABC):

    @abstractmethod
    async def put_document(
        self,
        filename: str,
        file_url: str,
        document_name: str,
        user_id: int,
        participiant_id: int,
    ) -> T: ...

    @abstractmethod
    async def get_all(self, offset: int, limit: int, **filters: Any) -> List[T]: ...

    @abstractmethod
    async def delete(self, **filters: Any) -> T | None: ...

    @abstractmethod
    async def update_status(
        self, request: Type[BaseModel], **filters: Any
    ) -> T | None: ...

    @abstractmethod
    async def get(self, **filters: Any) -> T | Any: ...
