import logging
from typing import Annotated

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer

from application.infrastructure.verifyer.user.exist_user import ExistUserVerifyer
from application.infrastructure.verifyer.user.verifying_of_existing_user import (
    ExistUserVerifyer,
)
from src.application.core.constants.constants import constants
from src.application.core.protocols.service import BaseService
from src.application.core.protocols.verifyer import BaseVerifyer
from src.application.infrastructure.repository.user import UserRepository
from src.application.infrastructure.verifyer.auth.token_verifyer import TokenVerifyer
from src.application.services.user.queries.get_user import GetUser
from src.application.services.user.scheme import SUser
from src.application.utils.utils import get_logger
from src.application.core.database.database import get_session
from sqlalchemy.ext.asyncio import AsyncSession

log: logging.Logger = get_logger()

oauth2_password_bearer: OAuth2PasswordBearer = OAuth2PasswordBearer(constants.URLS.AUTH_URL)

class GetCurrentUserDep:
    def __init__(
        self, get_user: BaseService, token_verifyer: BaseVerifyer, token: str
    ) -> None:
        self.get_user = get_user
        self.token_verifyer = token_verifyer
        self.token = token

    async def execute(self) -> SUser:

        # Get and verify token, if not valid, raise HTTPException 403
        sub: int = await self.token_verifyer.veirfy(self.token)
        log.info("Sub data | ID | %s", sub)

        return self.get_user.execute(user_id=sub)




async def get_user_repository(
    session: Annotated[AsyncSession, Depends(get_session)]
) -> UserRepository:
    return UserRepository(session=session)



async def exist_user_verifyer(
    repository: Annotated[UserRepository, Depends(get_user_repository)]
) -> ExistUserVerifyer:
    return ExistUserVerifyer(repository=repository)



async def get_token_verifyer() -> TokenVerifyer:
    return TokenVerifyer()




async def get_current_user(
    token: Annotated[str, Depends(oauth2_password_bearer)],

) 