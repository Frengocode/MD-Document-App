import logging

from fastapi.encoders import jsonable_encoder

from src.application.core.protocols.service import BaseService
from src.application.core.protocols.verifyer import BaseVerifyer
from src.application.services.user.models import User
from src.application.services.user.scheme import SUser
from src.application.utils.utils import get_logger

log: logging.Logger = get_logger()


class GetUser(BaseService):
    def __init__(
        self,
        verify_of_existing_user: BaseVerifyer,
    ) -> None:
        self.verify_of_existing_user = verify_of_existing_user

    async def execute(self, user_id: int) -> SUser:
        user: User = await self.verify_of_existing_user.verify(id=user_id)
        log.info("User was got | ID | %s", user)
        return SUser.model_validate(jsonable_encoder(user))
