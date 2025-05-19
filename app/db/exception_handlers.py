import re
from sqlalchemy.exc import IntegrityError
from app.exceptions import UniqueError, NotNullConstraintViolationException

class UniqueExceptionHandler:
    UNIQUE_VIOLATION_REGEX = re.compile(
        r'duplicate key value violates unique constraint "(?P<constraint>.+)"')

    def handle_exception(self, error: IntegrityError) -> None:
        match = self.UNIQUE_VIOLATION_REGEX.search(str(error.orig))
        if match:
            constraint_name = match.group("constraint")
            raise UniqueError(
                f"Пользователь с {constraint_name} уже существует!") from error
      # Если исключение не распознано, ничего не делает


class NotNullConstraintExceptionHandler:
    NOT_NULL_VIOLATION_REGEX = re.compile(r'null value in column "(?P<column>.+)" violates not-null constraint"')

    def handle_exception(self, error: IntegrityError) -> None:
        error_message = str(error.orig)
        match = self.NOT_NULL_VIOLATION_REGEX.search(error_message)
        if match:
            column_name = match.group("column")
            raise NotNullConstraintViolationException(
                f"Поле '{column_name}' обязательно для заполнения.") from error
        # Если исключение не распознано, ничего не делает