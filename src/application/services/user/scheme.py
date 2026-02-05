from enum import Enum
from typing import Self

from pydantic import BaseModel, model_validator

from src.application.services.user.exception import ShortPasswordException


class Role(str, Enum):
    USER = "user"
    CHEKER = "cheker"


class SAuthUserRequest(BaseModel):
    username: str
    password: str


class SCreateUserRequest(BaseModel):
    username: str
    password: str
    role: Role

    @model_validator(mode="after")
    def validate_password(self) -> Self:
        if len(self.password.encode("utf-8")) < 8:
            raise ShortPasswordException()
        return self


class SUser(BaseModel):
    id: int
    username: str
    role: str
    password: str


class SUpdateUserRequest(BaseModel):
    username: str
