from typing import Annotated

from fastapi import Depends
from fastapi.security import OAuth2PasswordRequestForm

from src.application.services.user.commands.auth_user import AuthUser
from src.application.services.user.dependcies.v1.dependcies import get_auth_user

GetAuthUserDep = Annotated[AuthUser, Depends(get_auth_user)]
Oauth2PasswordRequestFormDep = Annotated[OAuth2PasswordRequestForm, Depends()]
