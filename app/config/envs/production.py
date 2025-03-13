from pydantic_settings import BaseSettings

class ProductionConfig(BaseSettings):
    env: str = 'production'
    # CORS settings
    cors_origins: list[str] = ["https://example.com"]
    cors_allow_credentials: bool = True
    cors_allow_methods: list[str] = ["GET", "POST", "PUT", "DELETE"]
    cors_allow_headers: list[str] = ["*"]

    
  
    

