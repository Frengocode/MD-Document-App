import logging
from typing import Annotated

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession

from src.application.core.constants.constants import constants
from src.application.core.database.database import get_session
from src.application.core.protocols.service import BaseService
from src.application.core.protocols.verifyer import BaseVerifyer
from src.application.infrastructure.repository.user import UserRepository
from src.application.infrastructure.verifyer.auth.token_verifyer import TokenVerifyer
from src.application.infrastructure.verifyer.user.exist_user_verifyer import (
    ExistUserVerifyer,
)
from src.application.infrastructure.verifyer.user.get_user_verifyer import (
    GetUserVeifyer,
)
from src.application.infrastructure.verifyer.user.password_verifyer import (
    PasswordVeryfier,
)
from src.application.infrastructure.verifyer.user.verifying_of_existing_user import (
    VerifyOfExistingUser,
)
from src.application.services.user.commands.auth_user import AuthUser
from src.application.services.user.queries.get_user import GetUser
from src.application.services.user.scheme import SUser
from src.application.utils.utils import get_logger

log: logging.Logger = get_logger()

oauth2_password_bearer: OAuth2PasswordBearer = OAuth2PasswordBearer(
    constants.URLS.AUTH_URL
)


class GetCurrentUserDep:
    def __init__(
        self, get_user: BaseService, token_verifyer: BaseVerifyer, token: str
    ) -> None:
        self.get_user = get_user
        self.token_verifyer = token_verifyer
        self.token = token

    async def execute(self) -> SUser:

        # Get and verify token, if not valid, raise HTTPException 403
        sub: int = await self.token_verifyer.verify(self.token)
        log.info("Sub data | ID | %s", sub)

        return await self.get_user.execute(user_id=sub)


async def get_user_repository(
    session: Annotated[AsyncSession, Depends(get_session)],
) -> UserRepository:
    return UserRepository(session=session)


async def exist_user_verifyer(
    repository: Annotated[UserRepository, Depends(get_user_repository)],
) -> ExistUserVerifyer:
    return ExistUserVerifyer(repository=repository)


async def get_token_verifyer() -> TokenVerifyer:
    return TokenVerifyer()


async def verify_of_existing_user(
    repository: Annotated[UserRepository, Depends(get_user_repository)],
) -> VerifyOfExistingUser:
    return VerifyOfExistingUser(repository=repository)


async def get_user(
    verify_of_existing_user: Annotated[
        GetUserVeifyer, Depends(verify_of_existing_user)
    ],
) -> GetUser:
    return GetUser(verify_of_existing_user=verify_of_existing_user)


async def get_current_user(
    get_user: Annotated[GetUser, Depends(get_user)],
    token_verifyer: Annotated[TokenVerifyer, Depends(get_token_verifyer)],
    token: Annotated[str, Depends(oauth2_password_bearer)],
) -> SUser:
    current_user_dep: GetCurrentUserDep = GetCurrentUserDep(
        get_user=get_user, token_verifyer=token_verifyer, token=token
    )
    return await current_user_dep.execute()


async def password_verifyer() -> PasswordVeryfier:
    return PasswordVeryfier()


async def get_user_verifyer(
    repository: Annotated[UserRepository, Depends(get_user_repository)],
) -> GetUserVeifyer:
    return GetUserVeifyer(repository=repository)


async def get_auth_user(
    password_verifyer: Annotated[PasswordVeryfier, Depends(password_verifyer)],
    get_user_verifyer: Annotated[GetUserVeifyer, Depends(get_user_verifyer)],
) -> AuthUser:
    return AuthUser(
        password_verifyer=password_verifyer, get_user_verifyer=get_user_verifyer
    )
