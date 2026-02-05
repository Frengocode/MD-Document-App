from typing import Annotated, List

from fastapi import APIRouter, Depends, Path, Query

from src.application.infrastructure.repository.user import UserRepository
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
from src.application.services.user.commands.create_user import CreateUser
from src.application.services.user.commands.update_user import UpdateUser
from src.application.services.user.queries.get_users import GetUsers
from src.application.services.user.dependcies.v1.dependcies import (
    exist_user_verifyer,
    get_current_user,
    get_user_repository,
    get_user_verifyer,
    password_verifyer,
    verify_of_existing_user,
)
from src.application.services.user.queries.get_user import GetUser
from src.application.services.user.scheme import (
    SAuthUserRequest,
    SCreateUserRequest,
    SUpdateUserRequest,
    SUser,
)

user_router_service: APIRouter = APIRouter(
    prefix="/users/api/v1", tags=["User Service"]
)


@user_router_service.post("/create/user", response_model=SUser)
async def create_user(
    request: SCreateUserRequest,
    repository: Annotated[UserRepository, Depends(get_user_repository)],
    exist_user_verifyer: Annotated[ExistUserVerifyer, Depends(exist_user_verifyer)],
) -> SUser:
    service: CreateUser = CreateUser(
        exist_user_verify=exist_user_verifyer, repository=repository
    )
    return await service.execute(request=request)


@user_router_service.get("/get/user/{id}", response_model=SUser)
async def get_user(
    id: Annotated[int, Path(...)],
    verifying_of_existing_user: Annotated[
        VerifyOfExistingUser, Depends(verify_of_existing_user)
    ],
) -> SUser:
    service: GetUser = GetUser(verify_of_existing_user=verifying_of_existing_user)
    return await service.execute(user_id=id)


@user_router_service.post("/auth/user", response_model=SUser)
async def auth_user(
    request: SAuthUserRequest,
    password_verifyer: Annotated[PasswordVeryfier, Depends(password_verifyer)],
    get_user_verifyer: Annotated[GetUserVeifyer, Depends(get_user_verifyer)],
) -> SUser:
    service: AuthUser = AuthUser(
        password_verifyer=password_verifyer, get_user_verifyer=get_user_verifyer
    )
    return await service.execute(request=request)


@user_router_service.put("/user/update", response_model=SUser)
async def update_user(
    request: SUpdateUserRequest,
    current_user: Annotated[SUser, Depends(get_current_user)],
    repository: Annotated[UserRepository, Depends(get_user_repository)],
) -> SUser:
    service: UpdateUser = UpdateUser(repository=repository)
    return await service.execute(request=request, current_user=current_user)



@user_router_service.get(
    "/get/users/",
    response_model=List[SUser]
)
async def get_users(
    offset: Annotated[int, Query(...)],
    limit: Annotated[int, Query(...)],
    repository: Annotated[UserRepository, Depends(get_user_repository)]
) -> List[GetUsers]:
    service: GetUsers = GetUsers(repository=repository)
    return await service.execute(offset=offset, limit=limit)