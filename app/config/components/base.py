from pydantic_settings import BaseSettings
from app.config.constants import ENV_FILE_PATH
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent


class BaseConfig(BaseSettings):
    env: str = "development"
    app_host: str
    app_port: int

    class Config:
        env_file = ENV_FILE_PATH
        env_file_encoding = 'utf-8'
