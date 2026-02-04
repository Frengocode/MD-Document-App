import logging

from fastapi.encoders import jsonable_encoder

from application.core.protocols.verifyer import BaseVerifyer
from src.application.core.protocols.service import BaseService
from src.application.core.repository.user import ABCUserRepository
from src.application.services.user.models import User
from src.application.services.user.scheme import SAuthUserRequest, SUser
from src.application.utils.utils import get_logger

log: logging.Logger = get_logger()


class AuthUser(BaseService):
    def __init__(
        self,
        password_verifyer: BaseVerifyer,
        verifying_existing_of_user: BaseVerifyer,
        repository: ABCUserRepository,
    ) -> None:
        self.password_verifyer = password_verifyer
        self.verifying_existing_of_user = verifying_existing_of_user
        self.repository = repository

    async def execute(self, request: SAuthUserRequest) -> SUser | None:

        # Cheking existing of user
        # Returns user or HTTPException 404
        user: User = await self.verifying_existing_of_user.veirfy(
            username=request.username
        )

        log.info("User was got | %s", user.id)

        # Checks password
        await self.password_verifyer.veirfy(user=user, password=request.password)

        return SUser.model_validate(jsonable_encoder(user))
