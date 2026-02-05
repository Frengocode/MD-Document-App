from fastapi import APIRouter

from src.application.services.auth.command.login import Login
from src.application.services.auth.dependcies.v1.dependcies import (
    GetAuthUserDep,
    Oauth2PasswordRequestFormDep,
)
from src.application.services.auth.scheme import SLogin

auth_service_router: APIRouter = APIRouter(
    prefix="/auth/service/api/v1", tags=["Auth Service"]
)


@auth_service_router.post("/login", response_model=SLogin)
async def login(
    request: Oauth2PasswordRequestFormDep, get_auth_user_dep: GetAuthUserDep
) -> SLogin:
    service: Login = Login(get_auth_user=get_auth_user_dep)
    return await service.execute(request=request)
