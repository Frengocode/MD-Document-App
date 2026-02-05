import logging

from src.application.core.protocols.verifyer import BaseVerifyer
from src.application.core.repository.user import ABCUserRepository
from src.application.services.user.exception import UserNotFoundException
from src.application.services.user.models import User
from src.application.utils.utils import get_logger

log: logging.Logger = get_logger()


class GetUserVeifyer(BaseVerifyer):
    def __init__(self, repository: ABCUserRepository) -> None:
        self.repository = repository

    async def verify(self, username: int) -> User:
        user: User = await self.repository.get(username=username)
        if not user:
            log.info("User not found | USERNAME | %s", username)
            raise UserNotFoundException()
        return user
