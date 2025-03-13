from pydantic_settings import BaseSettings

class DevelopmentConfig(BaseSettings):
    env: str = 'development'
    # CORS settings
    cors_origins: list[str] = ["*"]
    cors_allow_credentials: bool = True
    cors_allow_methods: list[str] = ["*"]
    cors_allow_headers: list[str] = ["*"]