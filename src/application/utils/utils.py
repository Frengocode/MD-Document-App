import base64
import hashlib
import logging
from datetime import datetime, timedelta
from typing import Optional

import bcrypt
from jose import jwt
from passlib.context import CryptContext

from src.application.core.config.config import settings
from src.application.core.constants.constants import constants


def get_logger() -> logging.Logger:
    logging.basicConfig(level=logging.INFO)
    return logging.getLogger()


pwd_password: CryptContext = CryptContext(schemes=[constants.ALGORITMS.bcrypt])


def password_hasher(password: str) -> str:
    # 1️⃣ Pre-hash with SHA256 to handle long passwords safely
    prehashed = hashlib.sha256(password.encode("utf-8")).digest()

    # 2️⃣ Base64 encode to prevent NULL bytes / special chars
    encoded = base64.b64encode(prehashed)  # still bytes

    # 3️⃣ Hash with bcrypt (returns bytes)
    hashed = bcrypt.hashpw(encoded, bcrypt.gensalt())

    # 4️⃣ Convert to string for storage in DB
    return hashed.decode("utf-8")


# Verify a password (login)
def verify_password(plain_password: str, hashed_password: str) -> bool:
    # 1️⃣ Pre-hash the input like in hasher
    prehashed = hashlib.sha256(plain_password.encode("utf-8")).digest()
    encoded = base64.b64encode(prehashed)

    # 2️⃣ bcrypt.checkpw expects bytes
    return bcrypt.checkpw(encoded, hashed_password.encode("utf-8"))


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    to_encode = data.copy()

    # Преобразуем sub в строку, если оно не строка
    if "sub" in to_encode:
        to_encode["sub"] = str(to_encode["sub"])

    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(days=7)

    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(
        to_encode, settings.AUTH.AUTH_SECRET_KEY.get_secret_value(), algorithm="HS256"
    )
    return encoded_jwt
