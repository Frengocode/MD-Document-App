from typing import List

from fastapi.encoders import jsonable_encoder

from src.application.core.protocols.service import BaseService
from src.application.core.repository.user import ABCUserRepository
from src.application.services.user.models import User
from src.application.services.user.scheme import SUser


class GetUsers(BaseService):
    def __init__(self, repository: ABCUserRepository) -> None:
        self.repository = repository

    async def execute(self, offset: int, limit: int) -> List[SUser]:

        users: List[User] = await self.repository.get_all(offset=offset, limit=limit)
        return [SUser.model_validate(jsonable_encoder(user)) for user in users]
