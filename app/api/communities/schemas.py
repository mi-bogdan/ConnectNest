
from pydantic import BaseModel, ConfigDict
from fastapi import UploadFile, File
from typing import Annotated, Optional

import uuid


class CreateCommunities(BaseModel):
    title: str
    description: Optional[str] = None


class ShowCommunities:
    title: str
    description: str
    image_logo: str


class CommunityAll(BaseModel):
    id: uuid.UUID
    title: str
    description: str
    image_logo: str

    model_config = ConfigDict(from_attributes=True)


class CommunityAllAdmin(CommunityAll):
    admin_id: uuid.UUID

    
