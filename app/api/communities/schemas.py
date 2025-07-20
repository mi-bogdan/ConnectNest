from pydantic import BaseModel
from fastapi import UploadFile
from typing import Optional


class CreateCommunities(BaseModel):
    title: str
    description: Optional[str] = None


class ShowCommunities:
    title: str
    description: str
    image_logo: str
