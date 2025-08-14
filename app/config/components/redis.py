from pydantic_settings import BaseSettings
from app.config.constants import ENV_FILE_PATH


class RedisConfig(BaseSettings):
    redis_host: str
    redis_port: int
    redis_db: int
    redis_password: str = ''
    redis_username: str = ''

    def get_redis_url(self) -> str:
        if self.redis_password:
            return f"redis://{self.redis_username}:{self.redis_password}@{self.redis_host}:{self.redis_port}/{self.redis_db}"
        return f"redis://{self.redis_host}:{self.redis_port}/{self.redis_db}"

    class Config:
        env_file = ENV_FILE_PATH
        env_file_encoding = 'utf-8'
