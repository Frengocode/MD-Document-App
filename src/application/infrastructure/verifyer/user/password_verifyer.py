import logging

from src.application.core.protocols.verifyer import BaseVerifyer
from src.application.services.user.exception import InCorrectPasswordException
from src.application.services.user.models import User
from src.application.utils.utils import get_logger, verify_password

log: logging.Logger = get_logger()


class PasswordVeryfier(BaseVerifyer):
    async def verify(self, user: User, password: str) -> None:
        if not verify_password(password, user.password):
            log.info("Passoword didn't mathing")
            raise InCorrectPasswordException()
