from datetime import datetime, timedelta, timezone
import jwt
from pathlib import Path
from app.config import settings
from app.utils.mixins import LoggerMixin


class JWTManager(LoggerMixin):
    def __init__(
            self,
            private_key_path: Path,
            public_key_path: Path,
            algorithm: str,
    ):
        """
        Инициализация менеджера JWT.

        :param private_key_path: Путь к файлу с приватным ключом.
        :param public_key_path: Путь к файлу с публичным ключом.
        :param algorithm: Алгоритм шифрования.
        """

        self.private_key = private_key_path.read_text()
        self.public_key = public_key_path.read_text()
        self.algorithm = algorithm

    def encode_jwt(self, payload: dict, expire_minutes: int, expire_timedelta: timedelta | None = None):
        """
        Кодируем данные в JWT-токен.

        :param payload: Данные для кодирования.
        :return: Закодированный JWT-токен.
        """
        self.logger.debug("Кодирование JWT токена")
        now = datetime.now(timezone.utc)
        if expire_timedelta:
            expire = now + expire_timedelta
        else:
            expire = now + timedelta(minutes=expire_minutes)
        to_encode = payload.copy()
        to_encode.update(exp=expire, iat=now)
        encoded_jwt = jwt.encode(
            to_encode,
            self.private_key,
            algorithm=self.algorithm
        )
        return encoded_jwt

    def decode_jwt(self, token: str | bytes):
        """
        Декодирует JWT-токен.

        :param token: JWT-токен для декодирования.
        :return: Декодированные данные.
        """
        self.logger.debug("Декодирование JWT токена")

        if isinstance(token, str):
            token = token.encode("utf-8")

        decoded_jwt = jwt.decode(
            token,
            self.public_key,
            algorithms=[self.algorithm]
        )
        return decoded_jwt


def get_jwt_manager() -> JWTManager:
    return JWTManager(
        private_key_path=settings.private_key_path,
        public_key_path=settings.public_key_path,
        algorithm=settings.algorithm,
    )
