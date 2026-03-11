import os
import json
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent.parent
SRC_DIR = os.path.join(ROOT_DIR, "src")
ENVS_DIR = os.path.join(ROOT_DIR, "envs")

ENV_FLAG = os.getenv("ENV", "dev")  # register into os envs, default is dev
CONFIG_PATH = os.path.join(ENVS_DIR, f'config.{ENV_FLAG}.json')  # read config dynamically


class Settings:
    """app settings"""

    @staticmethod
    def _load() -> dict:
        with open(CONFIG_PATH, mode='rt', encoding='utf-8') as fp:
            return json.load(fp=fp)

    def __init__(self):
        self.config_dict = self._load()
        # basic
        self.env: str = self.config_dict['env']
        self.debug: bool = self.config_dict['debug']

        # DB
        self.postgres_user: str = self.config_dict['db']['user']
        self.postgres_password: str = self.config_dict['db']['password']
        self.postgres_db: str = self.config_dict['db']['name']
        self.database_url: str = self.config_dict['db']['url']

        # cache
        self.redis_host: str = self.config_dict['cache']['host']
        self.redis_port: int = self.config_dict['cache']['port']
        self.redis_password: str = self.config_dict['cache']['password']

        # jwt
        self.access_token_ttl: int = self.config_dict['jwt']['access_token_ttl']
        self.refresh_token_ttl: int = self.config_dict['jwt']['refresh_token_ttl']
        self.jwt_key: str = self.config_dict['jwt']['key']
        self.jwt_algo: str = self.config_dict['jwt']['algo']

        # cors
        self.cors_allow_origins: list[str] = self.config_dict['cors']['allow_origins']
        self.cors_allow_methods: list[str] = self.config_dict['cors']['allow_methods']
        self.cors_allow_credentials: bool = self.config_dict['cors']['allow_credentials']
        self.cors_allow_headers: list[str] = self.config_dict['cors']['allow_headers']


# use module level singleton
settings = Settings()
