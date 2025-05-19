from app.config.components.base import BaseConfig
from app.config.components.db import DatabaseConfig
from app.config.components.auth import Auth


class ComponentsConfig(BaseConfig, DatabaseConfig, Auth):
    pass


__all__ = ["ComponentsConfig"]
