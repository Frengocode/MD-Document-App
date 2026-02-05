from typing import Any, Protocol


class BaseVerifyer(Protocol):
    async def verify(self, *args: Any, **kwargs: Any) -> Any | None: ...
