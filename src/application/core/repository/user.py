from abc import ABC, abstractmethod
from typing import Any, List, Type, TypeVar

from pydantic import BaseModel

T = TypeVar("T")


class ABCUserRepository(ABC):

    @abstractmethod
    async def create(self, request: Type[BaseModel]) -> T: ...

    @abstractmethod
    async def get(self, **filters: Any) -> T | None: ...

    @abstractmethod
    async def get_all(self, offset: int, limit: int, **filters: Any) -> List[T]: ...

    @abstractmethod
    async def update(self, request: Type[BaseModel], **filters: Any) -> T: ...
