from pathlib import Path
from pydantic_settings import BaseSettings

from app.config.constants import ROOT_DIR


class Auth(BaseSettings):
    private_key_path: Path = ROOT_DIR / "config" / "certs" / "jwt-private.pem"
    public_key_path: Path = ROOT_DIR / "config" / "certs" / "jwt-public.pem"
    algorithm: str = "RS256"
    access_token_expire_minutes: int = 10 # минуты
    refresh_token_expire_days: int = 30 # дни
