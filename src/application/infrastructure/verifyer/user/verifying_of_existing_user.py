import logging

from src.application.core.protocols.verifyer import BaseVerifyer
from src.application.core.repository.user import ABCUserRepository
from src.application.services.user.exception import UserNotFoundException
from src.application.utils.utils import get_logger

log: logging.Logger = get_logger()


class ExistUserVerifyer(BaseVerifyer):
    def __init__(self, repository: ABCUserRepository) -> None:
        self.repository = repository

    async def verify(self, id: int) -> None:
        if await self.repository.get(id=id):
            log.info("User not found | ID | %s ", id)
            raise UserNotFoundException()
