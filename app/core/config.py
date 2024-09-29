import secrets
from typing import Annotated, Any, Literal

from pydantic import (
    AnyUrl,
    HttpUrl,
    BeforeValidator,
    MariaDBDsn,
    computed_field
)
from pydantic_core import Url
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing_extensions import Self


def parse_cors(v: Any) -> list[str] | str:
    if isinstance(v, str) and not v.startswith("["):
        return [i.strip() for i in v.split(",")]
    elif isinstance(v, list | str):
        return v
    raise ValueError(v)


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file="../.env",
        env_ignore_empty=True,
        extra="ignore",
    )
    API_V1_STR: str = "/api/v1"
    SECRET_KEY: str = secrets.token_urlsafe(32)
    FRONTEND_HOST: str = "http://localhost:3000"
    ENVIRONMENT: Literal["local", "staging", "production"] = "local"

    BACKEND_CORS_ORIGINS: Annotated[
        list[AnyUrl] | str, BeforeValidator(parse_cors)
    ] = []

    @computed_field
    @property
    def all_cors_origins(self) -> list[str]:
        return [str(origin).rstrip("/") for origin in self.BACKEND_CORS_ORIGINS] + [
            self.FRONTEND_HOST
        ]
    
    KAKAO_AUTH_ROOT_URL: str
    KAKAO_AUTH_CODE_PATH: str
    KAKAO_CLIENT_ID: str
    KAKAO_REDIRECT_URI: str
    KAKAO_RESPONSE_TYPE: str
    KAKAO_SCOPE: str

    @computed_field
    @property
    def KAKAO_AUTH_CODE_URI(self) -> str:
        return f"{self.KAKAO_AUTH_ROOT_URL}{self.KAKAO_AUTH_CODE_PATH}?client_id={self.KAKAO_CLIENT_ID}&redirect_uri={self.KAKAO_REDIRECT_URI}&response_type={self.KAKAO_RESPONSE_TYPE}&scope={self.KAKAO_SCOPE}"

    PROJECT_NAME: str = "runacer"
    SENTRY_DSN: HttpUrl | None = None
    MIRIA_SERVER: str
    MIRIA_PORT: int = 3306
    MIRIA_USER: str
    MIRIA_PASSWORD: str
    MIRIA_DB: str
    MARIA_OPTION: str

    @computed_field
    @property
    def SQLALCHEMY_DATABASE_URI(self) -> MariaDBDsn:
        return Url.build(
            scheme="mariadb+pymysql",
            username=self.MIRIA_USER,
            password=self.MIRIA_PASSWORD,
            host=self.MIRIA_SERVER,
            port=self.MIRIA_PORT,
            path=self.MIRIA_DB,
        )


settings = Settings()
