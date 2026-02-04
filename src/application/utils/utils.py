import logging
from datetime import datetime, timedelta

from jose import jwt
from passlib.context import CryptContext

from src.application.core.config.config import settings
from src.application.core.constants.constants import constants


def get_logger() -> logging.Logger:
    logging.basicConfig(level=logging.INFO)
    return logging.getLogger()


pwd_password: CryptContext = CryptContext(schemes=[constants.ALGORITMS.bcrypt])


def password_hasher(password: str) -> str:
    return pwd_password.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_password.verify(plain_password, hashed_password)


def create_access_token(data: dict, expires_delta: timedelta) -> str:
    to_encode = data.copy()

    if "sub" in to_encode:
        to_encode["sub"] = str(to_encode["sub"])

    expire = datetime.utcnow() + expires_delta

    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(
        to_encode,
        settings.AUTH.AUTH_SECRET_KEY.get_secret_value(),
        algorithm=constants.ALGORITMS.HS256,
    )
    return encoded_jwt
