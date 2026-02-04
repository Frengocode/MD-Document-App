from typing import Any, List, Optional, Protocol, Union

from pydantic import BaseModel


class BaseService(Protocol):

    async def execute(
        self, *args: Any, **kwargs: Any
    ) -> Optional[Union[BaseModel, List[BaseModel]]]: ...
