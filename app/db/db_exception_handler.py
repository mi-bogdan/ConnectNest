from app.exceptions import ApplicationException, DatabaseException
from typing import List

from .exception_handlers import UniqueExceptionHandler,NotNullConstraintExceptionHandler

class DBExceptionHandler:
    def __init__(self, handlers: List):
        self.handlers = handlers

    def handle_exception(self, error) -> None:
        """
        Анализирует исключение и вызывает соответствующий пользовательский обработчик.

        :param error: Исключение, полученное при выполнении операции в базе данных.
        """
        for handler in self.handlers:
            try:
                handler.handle_exception(error)
                return  # Если обработчик обработал исключение, выходим из цикла
            except ApplicationException as exc:
                raise exc  # Пробрасываем пользовательское исключение
        # Если ни один обработчик не распознал исключение
        raise DatabaseException("Ошибка базы данных.") from error
    


def get_db_exception_handler() -> DBExceptionHandler:
    handler = [
        UniqueExceptionHandler(),
        NotNullConstraintExceptionHandler()

    ]
    return DBExceptionHandler(handler)
    
