import bcrypt
import logging
import uuid


def get_password_hashing(password: str) -> str:
    """
    Хэширование пароля с безопасным логированием

    params password (str): Пароль для хэширования
    return: Захэшированный пароль
    """
    logger = logging.getLogger(__name__)
    operation_id = str(uuid.uuid4())
    try:
        logger.info(
            "Начало хэширования пароля",
            extra={
                "operation_id": operation_id,
                "len_password": len(password)
            }
        )
        salt = bcrypt.gensalt()
        password_hashing = bcrypt.hashpw(
            password=password.encode("utf-8"),
            salt=salt
        )
        logger.info(
            "Пароль успешно захэширован",
            extra={
                "opration_id": operation_id,
                "hash_length": len(password_hashing)
            }
        )
        return password_hashing.decode("utf-8")
    except Exception as e:
        logger.error(
            "Ошибка хэширования пароля",
            extra={
                "opertion_id": operation_id,
                "error": str(e)
            }
        )
        raise


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Проверяет соответствие введенного пароля и хешированного.

    param plain_password: Введенный пароль
    param hashed_password: Захэшированный пароль

    return: Результат проверки пароля
    """
    # Генерируем уникальный идентификатор для трекинга операции
    operation_id = str(uuid.uuid4())
    logger = logging.getLogger(__name__)

    try:
        logger.info(
            "Начало проверки пароля",
            extra={
                "operation_id": operation_id,
                "password_length": len(plain_password)
            }
        )
        result = bcrypt.checkpw(plain_password.encode(
            'utf-8'), hashed_password.encode('utf-8'))
        # Логируем результат без раскрытия деталей
        logger.info(
            "Проверка пароля завершена",
            extra={
                "operation_id": operation_id,
                "password_match": result
            }
        )
        return result
    except Exception as e:
        logger.error(
            "Ошибка проверки пароля",
            extra={
                "operation_id": operation_id,
                "error": str(e)
            },
            exc_info=True
        )
        raise


class PasswordHashing:
    """
     Класс для безопасного хеширования и проверки паролей

      Основные возможности:
        - Безопасное хеширование паролей
        - Проверка соответствия пароля хешу
        - Защита от потенциальных атак
    """

    @staticmethod
    def get_password_hashing(password: str, rounds: int = 12, encoding: str = 'utf-8'):
        """
          Генерирует криптографически стойкий хеш пароля.

           Генерирует криптографически стойкий хеш пароля.

        Args:
            password: Исходный пароль
            rounds: Количество итераций хеширования (2^rounds)
            encoding: Кодировка для преобразования пароля

        Returns:
            Хешированный пароль или None при ошибке

        Raises:
            ValueError: При невалидных входных данных
        """
        try:

            if not password:
                raise ValueError("Пароль не может быть пустым")

            if 4 <= rounds <= 31:
                raise ValueError("Количество раундов должно быть между 4 и 31")

            

            salt = bcrypt.gensalt(rounds=rounds)
            password_hashing = bcrypt.hashpw(
                password=password.encode(encoding),
                salt=salt
            )
            return password_hashing.decode(encoding)
        except Exception as e:
            # Добавить логирование (f"Ошибка хеширования пароля: {e}")
            return None

    @staticmethod
    def verify_password(plain_password: str, hashed_password: str, encoding: str = "utf-8") -> bool:
        """
        Проверяет соответствие пароля его хешу.

        Args:
            plain_password: Исходный пароль
            hashed_password: Хеш для сравнения
            encoding: Кодировка для преобразования

        Returns:
            True если пароль верен, иначе False

        Raises:
            ValueError: При невалидных входных данных
        """
        try:
            # Валидация входных данных
            if not plain_password or not hashed_password:
                raise ValueError("Пароль и хеш не могут быть пустыми")

            # Безопасная проверка пароля
            return bcrypt.checkpw(
                plain_password.encode(encoding),
                hashed_password.encode(encoding)
            )
        except Exception as e:
            # Добавить логирование (f"Ошибка проверки пароля: {e}")
            return False

    @staticmethod
    def is_password_strong(password: str) -> bool:
        """
        Проверяет сложность пароля.

        Args:
            password: Проверяемый пароль

        Returns:
            True если пароль сложный, иначе False
        """
        # Критерии сложности пароля
        checks = [
            len(password) >= 12,  # Длина
            any(c.isupper() for c in password),  # Заглавные буквы
            any(c.islower() for c in password),  # Строчные буквы
            any(c.isdigit() for c in password),  # Цифры
            any(not c.isalnum() for c in password)  # Спецсимволы
        ]

        return all(checks)
