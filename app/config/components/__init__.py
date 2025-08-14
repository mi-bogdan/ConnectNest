from app.config.components.base import BaseConfig
from app.config.components.db import DatabaseConfig
from app.config.components.auth import Auth
from app.config.components.redis import RedisConfig


class ComponentsConfig(BaseConfig, DatabaseConfig, Auth,RedisConfig):
    pass


__all__ = ["ComponentsConfig"]
