import aiofiles
from pathlib import Path

from fastapi.params import Depends
from fastapi import UploadFile
from typing import Optional

from app.exceptions import InvalidImageExtension, FileSaveError
from app.core.enums import MediaType
from .media_manager import MediaManager, get_media_manager
from app.utils.mixins import LoggerMixin


ALLOWED_IMAGE_EXTENSIONS = {
    "png", "jpe", "jpeg", "jpg", "gif",
    "bmp", "ico", "webp", "tiff", "tif",
    "svg", "svgz", "apng", "jfif", "pjpeg", "pjp"
}


class ImageService(LoggerMixin):
    """Сервис обработка и сохранение визуальных объектов"""

    def __init__(self, media_type: MediaType, media_manager: MediaManager):
        self.media_type = media_type
        self.media_manager = media_manager

    def _get_file_extension(self, filename: str) -> str:
        """
        Получение и проверка расширения файла

        :param filename: Имя файла
        :return: Расширение файла
        :raises InvalidImageExtension: Если расширение не поддерживается
        """
        self.logger.info("Проверка расширения файла")
        parts = filename.split(".")
        file_type = parts[-1].lower()

        if file_type not in ALLOWED_IMAGE_EXTENSIONS:
            self.logger.warning(f"Не поддержуемы формат: {file_type}")
            raise InvalidImageExtension(
                f"Неподдерживаемый формат изображения: {file_type}"
            )
        return file_type

    def generate_filename(self, original_filename: str) -> Path:
        """
        Генерация уникального имени файла

        :param original_filename: Оригинальное имя файла
        :return: Путь к новому файлу
        """
        self.logger.info("Генераия уникального имени файла")
        import uuid

        # Получаем расширение файла
        file_extension = self._get_file_extension(original_filename)

        # Получаем путь для типа медиа
        media_type_path = self.media_manager.get_media_patch(self.media_type)

        # Генерируем уникальное имя
        unique_filename = f"{uuid.uuid4()}.{file_extension}"
        self.logger.info("Файл сгенерирован его имя: {unique_filename}")

        return media_type_path / unique_filename

    async def save_image(self, image: Optional[UploadFile] = None) -> str:
        """
        Сохранение изображения

        :param image: Файл изображения
        :return: Относительный путь к сохраненному изображению или None
        """
        self.logger.info("Сохранение изображения")
        if not image:
            self.logger.warning("Изображение небыло предоставлено")
            return ""

        try:
            # Генерация пути для файла
            file_path = self.generate_filename(image.filename)

            # Сохранение файла
            async with aiofiles.open(file_path, 'wb') as f:
                await f.write(await image.read())

            self.logger.info(f"Изображение сохранено {file_path}")
            return self.media_manager.get_relative_path(file_path)
        except InvalidImageExtension as e:
            self.logger.warning("Недопустимое расширение изображения")
            raise
        except Exception as e:
            self.logger.error(f"Ошибка при сохранении файла {e}")
            raise FileSaveError(f"Ошибка при сохранении файла {e}")


def get_image_service(media_manager: MediaManager = Depends(get_media_manager)):
    return ImageService(media_type=MediaType.COMMUNITY, media_manager=media_manager)
