from typing import Self

from pydantic import BaseModel, model_validator

from src.application.core.constants.constants import constants
from src.application.services.user.exception import (
    RoleException,
    ShortPasswordException,
)
from src.application.utils.utils import password_hasher


class SAuthUserRequest(BaseModel):
    username: set
    password: str


class SCreateUserRequest(BaseModel):
    username: str
    password: str
    role: str

    @model_validator(mode="after")
    def validate_password(self) -> str:
        if len(self.password) < 8:
            raise ShortPasswordException()
        return password_hasher(self)

    @model_validator(mode="after")
    def validate_role(self) -> Self:
        if not self.role == constants.ROLES.USER or constants.ROLES.CHEKER:
            raise RoleException()
        return self


class SUser(BaseModel):
    id: int
    username: str
    role: str


class SUpdateUserRequest(BaseModel):
    username: str
