from datetime import date

from fastapi.security import OAuth2PasswordRequestForm

from src.application.core.constants.constants import constants
from src.application.core.protocols.service import BaseService
from src.application.services.auth.scheme import SLogin
from src.application.services.user.scheme import SAuthUserRequest, SUser
from src.application.utils.utils import create_access_token


class Login(BaseService):
    def __init__(self, get_auth_user: BaseService) -> None:
        self.get_auth_user = get_auth_user

    async def execute(self, request: OAuth2PasswordRequestForm) -> SLogin:

        # Creating reqeust for get AuthUser
        auth_user_request: SAuthUserRequest = SAuthUserRequest(
            username=request.username, password=request.password
        )

        # Get user or raises HTTPException 400
        user: SUser = await self.get_auth_user.execute(request=auth_user_request)
        access_token: str = create_access_token(data={"sub": user.id})
        return SLogin(access_token=access_token)
