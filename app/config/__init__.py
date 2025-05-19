from app.config.components import ComponentsConfig
from app.config.envs.production import ProductionConfig
from app.config.envs.development import DevelopmentConfig


class DevelopmentSettings(ComponentsConfig, DevelopmentConfig):
    pass


class ProductionSettings(ComponentsConfig, ProductionConfig):
    pass


def get_settings() -> DevelopmentSettings | ProductionSettings:

    env = ComponentsConfig().env
    print(env)

    if env == "development":
        return DevelopmentSettings()
    elif env == "production":
        return ProductionSettings()
    else:
        raise ValueError(f"Unknown enviroment: {env}")


settings = get_settings()
