from config.components.base import BaseConfig
from config.components.db import DatabaseConfig


class ComponentsConfig(BaseConfig, DatabaseConfig):
    pass


__all__ = ["ComponentsConfig"]
