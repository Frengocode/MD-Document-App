from dotenv import load_dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict

load_dotenv("constants.env")


class Buckets(BaseSettings):
    """MinIO s3 buckets"""

    DOCUMENTS_BUCKET: str

    model_config: SettingsConfigDict = SettingsConfigDict(
        env_file=".constants.env", extra="allow"
    )


class Urls(BaseSettings):

    AUTH_URL: str
    GET_DOCUMENT_URL: str

    model_config: SettingsConfigDict = SettingsConfigDict(
        env_file="constants.env", extra="allow"
    )


class Algorithms(BaseSettings):
    HS256: str
    bcrypt: str

    model_config: SettingsConfigDict = SettingsConfigDict(
        env_file=".constants.env", extra="allow"
    )


class Token(BaseSettings):
    EXPIRES_DAYS: int

    model_config: SettingsConfigDict = SettingsConfigDict(
        env_file="constants.env", extra="allow"
    )


class Roles(BaseSettings):
    USER: str
    CHEKER: str

    model_config: SettingsConfigDict = SettingsConfigDict(
        env_file="constants.env", extra="allow"
    )


class Constants(BaseSettings):
    BUCKETS: Buckets = Buckets()
    URLS: Urls = Urls()
    ALGORITMS: Algorithms = Algorithms()
    TOKEN: Token = Token()
    ROLES: Roles = Roles()

    model_config: SettingsConfigDict = SettingsConfigDict(
        env_file="constants.env", extra="allow"
    )


constants: Constants = Constants()
