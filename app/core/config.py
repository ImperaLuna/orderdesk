from functools import lru_cache
from typing import Literal

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    app_name: str = "orderdesk"
    app_env: Literal["local", "test", "docker", "staging", "prod"] = "local"
    database_url: str = "sqlite+aiosqlite:///./orderdesk.db"
    log_level: str = "INFO"

    @property
    def is_prod(self) -> bool:
        return self.app_env == "prod"


@lru_cache
def get_settings() -> Settings:
    return Settings()
