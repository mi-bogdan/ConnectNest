from pydantic import BaseModel, EmailStr, field_validator
import uuid
import re


LETTER_MATCH_PATTERN = re.compile(r"^[а-яА-Яa-zA-Z0-9\-]*$")


class RegisterUsers(BaseModel):
    username: str
    email: EmailStr
    password: str

    @field_validator("username")
    @classmethod
    def validator_username(cls, value):
        if not LETTER_MATCH_PATTERN.match(value):
            raise ValueError("Username contains forbidden characters")
        if len(value) > 50:
            raise ValueError("The username is too long")
        if not value:
            raise ValueError("must not be empty string")
        return value


class ShowUsers(BaseModel):
    id: uuid.UUID
    username: str
    email: EmailStr

    class Config:
        from_attributes = True


class DeleteUserShow(BaseModel):
    id: uuid.UUID


class LoginUser(BaseModel):
    username: str
    password: str


class TokenInfo(BaseModel):
    access_token: str
    refresh_token: str | None = None
    token_type: str = "Bearer"
