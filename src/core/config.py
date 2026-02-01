import os
from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict


__all__ = [
    'settings'
]

ROOT_DIR = Path(__file__).resolve().parent.parent.parent
SRC_DIR = os.path.join(ROOT_DIR, "src")
ENVS_DIR = os.path.join(ROOT_DIR, "envs")

ENV = os.getenv("ENV", "dev")  # 注册到shell的变量列表，默认为dev


class Settings(BaseSettings):
    env: str = "dev"
    debug: bool = True
    database_url: str | None = None
    model_config = SettingsConfigDict(
        env_file=os.path.join(ENVS_DIR, f".env.{ENV}"),
        env_file_encoding="utf-8"
    )


# use module level singleton
settings = Settings()
