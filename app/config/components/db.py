from pydantic_settings import BaseSettings
from config.constants import ENV_FILE_PATH


class DatabaseConfig(BaseSettings):
    postgres_host: str 
    postgres_port: int 
    postgres_user: str 
    postgres_password: str 
    postgres_db: str 

    class Config:
        env_file = ENV_FILE_PATH
        env_file_encoding = 'utf-8'


