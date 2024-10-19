import os
from pathlib import Path, PosixPath
from typing import Annotated, Any, Literal, ClassVar

from pydantic import (
    AnyUrl,
    BeforeValidator,
    HttpUrl,
    PostgresDsn,
    computed_field,
)
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic_core import MultiHostUrl
from sqladmin.templating import Jinja2Templates


def parse_cors(v: Any) -> list[str] | str:
    if isinstance(v, str) and not v.startswith("["):
        return [i.strip() for i in v.split(",")]
    elif isinstance(v, list | str):
        return v
    raise ValueError(v)


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_ignore_empty=True, extra="ignore")
    API_V1_STR: str = "/api/v1"
    SECRET_KEY: str = os.getenv('SECRET_KEY')
    DOMAIN: str = "localhost:8000"
    ENVIRONMENT: Literal["local", "staging", "production"] = "local"
    BASE_PATH: PosixPath = Path(__file__).resolve().parent.parent.parent
    APP_DIR: PosixPath = BASE_PATH / "app"
    TEMPLATE: PosixPath = APP_DIR / "templates"
    ADMIN_TEMPLATE_DIR: PosixPath = TEMPLATE / "admin"
    ADMIN_TEMPLATES: ClassVar[Jinja2Templates] = Jinja2Templates(directory=str(ADMIN_TEMPLATE_DIR))

    @computed_field  # type: ignore[prop-decorator]
    @property
    def server_host(self) -> str:
        if self.ENVIRONMENT == "local":
            return f"http://{self.DOMAIN}"
        return f"https://{self.DOMAIN}"

    BACKEND_CORS_ORIGINS: Annotated[list[AnyUrl] | str, BeforeValidator(parse_cors)] = []

    PROJECT_NAME: str = "FastAPI"
    SENTRY_DSN: HttpUrl | None = None
    POSTGRES_SERVER: str = os.getenv('POSTGRES_SERVER')
    POSTGRES_PORT: int = 5432
    POSTGRES_USER: str = os.getenv('POSTGRES_USER')
    POSTGRES_PASSWORD: str = os.getenv('POSTGRES_PASSWORD')
    POSTGRES_DB: str = os.getenv('POSTGRES_PASSWORD')

    @computed_field  # type: ignore[prop-decorator]
    @property
    def SQLALCHEMY_DATABASE_URI(self) -> PostgresDsn:
        return str(
            MultiHostUrl.build(
                scheme="postgresql+asyncpg",
                username=self.POSTGRES_USER,
                password=self.POSTGRES_PASSWORD,
                host=self.POSTGRES_SERVER,
                port=self.POSTGRES_PORT,
                path=self.POSTGRES_DB,
            )
        )

settings = Settings()  # type: ignore
