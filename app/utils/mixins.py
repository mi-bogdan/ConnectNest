import logging


class LoggerMixin:
    @property
    def logger(self):
        return logging.getLogger(self.__class__.__name__)


class DataMaskinMixinEmail:

    @staticmethod
    def mask_email(email: str) -> str:
        """
        Маскировка email

        param email: Почта 

        return: Замаскированная почта
        """
        if not email:
            return "N/A"

        parts = email.split("@")

        if len(parts) != 2:
            return "Invalid email"

        parts_mask = parts[0][:2] + "*" * (len(parts[0])-2)
        return f"{parts_mask}@{parts[1]}"
