from typing import Any

from jose import jwt

from src.application.core.config.config import settings
from src.application.core.constants.constants import constants
from src.application.core.protocols.verifyer import BaseVerifyer
from src.application.services.auth.exceptions import BrokenTokenFoundException


class TokenVerifyer(BaseVerifyer):
    async def verify(self, token: str) -> int:
        payload: dict[str, Any] = jwt.decode(
            token=token,
            key=settings.AUTH.AUTH_SECRET_KEY.get_secret_value(),
            algorithms=constants.ALGORITMS.HS256,
        )
        if not payload["sub"]:
            raise BrokenTokenFoundException()
        return int(payload["sub"])
