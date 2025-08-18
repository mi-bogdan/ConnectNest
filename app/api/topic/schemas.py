from pydantic import BaseModel, field_validator
from uuid import UUID


class CreateTopic(BaseModel):
    title: str

    @field_validator("title")
    @classmethod
    def validation_title(cls, value: str):
        if not value or value.strip() == "":
            raise ValueError("Поле не может быть пустым!")
        return value.strip()


class ResponseTopic(BaseModel):
    id: UUID
    title: str

    class Config:
        from_attributes = True
