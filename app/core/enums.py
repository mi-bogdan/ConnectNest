from enum import Enum


class MediaType(Enum):
    USER = "user"
    POST = "post"
    COMMUNITY = "community"


class LogLevel(Enum):
    DEV = "developer"
    PROD = "production"
