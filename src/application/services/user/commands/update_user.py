import logging

from fastapi.encoders import jsonable_encoder

from src.application.core.protocols.service import BaseService
from src.application.core.repository.user import ABCUserRepository
from src.application.services.user.models import User
from src.application.services.user.scheme import SUpdateUserRequest, SUser
from src.application.utils.utils import get_logger

log: logging.Logger = get_logger()


class UpdateUser(BaseService):
    def __init__(self, repository: ABCUserRepository) -> None:
        self.repository = repository

    async def execute(self, request: SUpdateUserRequest, current_user: SUser) -> SUser:

        updated_user: User = await self.repository.update(
            request=request, id=current_user.id
        )
        log.info("User successfully updated ID | %s", updated_user.id)
        return SUser.model_validate(jsonable_encoder(updated_user))
