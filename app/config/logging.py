from app.core.enums import LogLevel
from .components.base import BASE_DIR
from pathlib import Path
import logging
from logging.handlers import RotatingFileHandler
import sys
from app.config import settings
from colorama import init, Fore, Style
from logging import StreamHandler


class ColoredFormatter(logging.Formatter):
    """Цветной форматтер для логов с поддержкой extra"""

    COLORS = {
        logging.DEBUG: Fore.CYAN,
        logging.INFO: Fore.GREEN,
        logging.WARNING: Fore.YELLOW,
        logging.ERROR: Fore.RED,
        logging.CRITICAL: Fore.MAGENTA + Style.BRIGHT
    }

    def format(self, record):
        # Извлекаем extra-поля
        extra_fields = {
            k: v for k, v in record.__dict__.items()
            if k not in ['args', 'asctime', 'created', 'exc_info', 'exc_text',
                         'filename', 'funcName', 'levelname', 'levelno', 'lineno',
                         'module', 'msecs', 'msg', 'name', 'pathname', 'process',
                         'processName', 'relativeCreated', 'thread', 'threadName']
        }

        # Добавляем extra-поля к сообщению, если они есть
        if extra_fields:
            extra_str = " | " + \
                " | ".join(f"{k}={v}" for k, v in extra_fields.items())
            record.msg = f"{record.msg}{extra_str}"

        # Получаем базовое форматирование
        log_message = super().format(record)

        # Определяем цвет в зависимости от уровня логирования
        color = self.COLORS.get(record.levelno, Fore.WHITE)

        # Цветное форматирование
        return f"{color}{log_message}{Style.RESET_ALL}"


class ColoredStreamHandler(StreamHandler):
    """Кастомный обработчик с цветным выводом"""

    def __init__(self, stream=sys.stdout):
        super().__init__(stream)
        # Инициализация colorama
        init(strip=False, convert=True)


class LoggerConfig:
    """Настройка конфигурации логирования с цветным выводом"""

    @staticmethod
    def setup_logger(
        level_logger: LogLevel = LogLevel.DEV,
        base_dir: Path = BASE_DIR,
        logs_root: str = "logs"
    ):
        logs_path = base_dir / logs_root
        logs_path.mkdir(exist_ok=True)

        logger = logging.getLogger()
        logger.handlers.clear()  # Очищаем существующие обработчики

        # Базовый формат лога
        log_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        date_format = '%Y-%m-%d %H:%M:%S'

        # Цветной форматтер
        colored_formatter = ColoredFormatter(
            fmt=log_format,
            datefmt=date_format
        )

        # Цветной консольный обработчик
        console_handler = ColoredStreamHandler(sys.stdout)
        console_handler.setFormatter(colored_formatter)

        # Файловый обработчик (без цвета для файла)
        file_formatter = logging.Formatter(
            fmt=log_format,
            datefmt=date_format
        )
        file_handler = RotatingFileHandler(
            logs_path / 'app.log',
            maxBytes=10*1024*1024,  # 10 MB
            backupCount=5
        )
        file_handler.setFormatter(file_formatter)

        # Настройка уровней логирования
        if level_logger == LogLevel.DEV:
            logger.setLevel(logging.DEBUG)
            console_handler.setLevel(logging.DEBUG)
            file_handler.setLevel(logging.DEBUG)
        else:
            logger.setLevel(logging.ERROR)
            console_handler.setLevel(logging.ERROR)
            file_handler.setLevel(logging.ERROR)

        # Добавляем обработчики
        logger.addHandler(console_handler)
        logger.addHandler(file_handler)

        return logger


class ExtendedConfigLogger:
    @classmethod
    def get_log_config(cls):
        log_level = (LogLevel.DEV if settings.env ==
                     "development" else LogLevel.PROD)
        return LoggerConfig.setup_logger(log_level)
