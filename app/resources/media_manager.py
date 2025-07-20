from pathlib import Path

from app.core.enums import MediaType
from app.config.components.base import BASE_DIR
from app.utils.mixins import LoggerMixin


class MediaManager(LoggerMixin):
    """Менеджер для управления медиа директорями"""

    def __init__(self, base_dir: Path = BASE_DIR, media_root: str = "media") -> None:
        """
        Инициализация менеджера медиа-файлов
        :param base_dir: Базовая директория проекта
        :param media_root: Название корневой медиа-директории
        """
        self.base_dir = base_dir
        self.media_root = media_root
        self.media_patch = base_dir / media_root

        # Создание медиа директори если не созданная
        self._create_media_root()

    def _create_media_root(self):
        """Создание корневой медиа-директории"""
        self.logger.info("Создание главной директории медиа файлов")

        self.media_patch.mkdir(exist_ok=True)

    def get_media_patch(self, media_type: MediaType) -> Path:
        """
        Получения пути для конкретного типа медиа

        :param media_type: Тип медиа
        :return: Путь к директори
        """
        self.logger.info(
            f"Получение Получения пути для конкретного типа медиа {media_type}")
        media_type_patch = self.media_patch / media_type.value

        media_type_patch.mkdir(exist_ok=True)
        return media_type_patch

    def get_relative_path(self, full_path: Path) -> str:
        """
        Получение относительного пути от корня проекта

        :param full_path: Полный путь к файлу
        :return: Относительный путь
        """
        self.logger.info("Получение относительного пути от корня проекта")
        return str(full_path.relative_to(self.base_dir)).replace('\\', '/')


def get_media_manager() -> MediaManager:
    return MediaManager()
