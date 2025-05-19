import bcrypt

def get_password_hashing(password: str) -> str:
    """Хэширование пароля"""
    salt = bcrypt.gensalt()
    password_hashing = bcrypt.hashpw(
        password=password.encode("utf-8"),
        salt=salt
    )
    return password_hashing.decode("utf-8")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Проверяет соответствие введенного пароля и хешированного."""
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))


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
            
            # Может добавить класс метод реализации проверку сложности пароля is_password_strong

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
            #Добавить логирование (f"Ошибка проверки пароля: {e}")
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
