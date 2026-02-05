import os
from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict

__all__ = ["app_settings", "infra_settings"]

ROOT_DIR = Path(__file__).resolve().parent.parent.parent
SRC_DIR = os.path.join(ROOT_DIR, "src")
ENVS_DIR = os.path.join(ROOT_DIR, "envs")

ENV = os.getenv("ENV", "dev")  # 注册到shell的变量列表，默认为dev


class AppSettings(BaseSettings):
    """app base settings"""

    env: str = "dev"
    debug: bool = True

    model_config = SettingsConfigDict(
        env_file=os.path.join(ENVS_DIR, f".env.{ENV}.app"),
        env_file_encoding="utf-8",
        extra="ignore",
    )


class InfraSettings(BaseSettings):
    """infrastructure settings(db, etc...)"""

    # DB
    POSTGRES_USER: str
    POSTGRES_PW: str
    POSTGRES_DB: str
    DATABASE_URL: str

    # cache
    REDIS_HOST: str
    REDIS_PORT: int
    REDIS_PASSWORD: str

    # jwt
    ACCESS_TOKEN_TTL: int
    REFRESH_TOKEN_TTL: int
    JWT_KEY: str
    JWT_ALGO: str

    model_config = SettingsConfigDict(
        env_file=os.path.join(ENVS_DIR, f".env.{ENV}.infra"),
        env_file_encoding="utf-8",
        extra="ignore",  # 目前还没在cls中定义的ENV变量可以忽略报错
    )


# use module level singleton
app_settings = AppSettings()
infra_settings = InfraSettings()
