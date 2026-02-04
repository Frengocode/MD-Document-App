import logging

from fastapi.encoders import jsonable_encoder

from application.core.protocols.verifyer import BaseVerifyer
from src.application.core.protocols.service import BaseService
from src.application.core.repository.user import ABCUserRepository
from src.application.services.user.models import User
from src.application.services.user.scheme import SCreateUserRequest, SUser
from src.application.utils.utils import get_logger

log: logging.Logger = get_logger()


class CreateUser(BaseService):
    def __init__(
        self, exist_user_verify: BaseVerifyer, repository: ABCUserRepository
    ) -> None:
        self.exist_user_verify = exist_user_verify
        self.repository = repository

    async def execute(self, request: SCreateUserRequest) -> SUser | None:

        # Checking exist user if exist
        await self.exist_user_verify.veirfy(username=request.username)

        # Creating user
        created_user: User = await self.repository.create(request=request)
        log.info("User created %s | ", created_user.id)

        return SUser.model_validate(jsonable_encoder(created_user))
