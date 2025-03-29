from pydantic_settings import BaseSettings
from config.constants import ENV_FILE_PATH


class DatabaseConfig(BaseSettings):
    postgres_host: str
    postgres_port: int
    postgres_user: str
    postgres_password: str
    postgres_db: str

    def get_database_string(self):
        database_string = f"postgresql+asyncpg://{self.postgres_user}:{self.postgres_password}@{self.postgres_host}:{self.postgres_port}/{self.postgres_db}"
        return database_string

    class Config:
        env_file = ENV_FILE_PATH
        env_file_encoding = 'utf-8'
