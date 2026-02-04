from typing import Any, Protocol


class BaseVerifyer(Protocol):
    async def veirfy(self, *args: Any, **kwargs: Any) -> Any | None: ...
