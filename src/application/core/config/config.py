from dotenv import load_dotenv
from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict

load_dotenv()


class PostgreSQLConfig(BaseSettings):
    PG_URL: SecretStr

    model_config: SettingsConfigDict = SettingsConfigDict(
        env_file=".env", extra="allow"
    )


class MinIOConfig(BaseSettings):
    MINIO_USERNAME: str
    MINIO_PASSWORD: str
    MINIO_HOST: str

    model_config: SettingsConfigDict = SettingsConfigDict(
        env_file=".env", extra="allow"
    )


class AuthConfig(BaseSettings):
    AUTH_SECRET_KEY: SecretStr

    model_config: SettingsConfigDict = SettingsConfigDict(
        env_file=".env", extra="allow"
    )


class Settings(BaseSettings):
    PG: PostgreSQLConfig = PostgreSQLConfig()
    MINIO: MinIOConfig = MinIOConfig()
    AUTH: AuthConfig = AuthConfig()

    model_config: SettingsConfigDict = SettingsConfigDict(
        env_file=".env", extra="allow"
    )


settings: Settings = Settings()
