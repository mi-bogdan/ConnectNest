from fastapi import Depends, HTTPException, APIRouter, status, Form, File, UploadFile
from typing import List, Optional, Annotated
from uuid import UUID
from app.api.auth.service import get_current_users
from .schemas import CreatePost
from .service import ServicePost,get_service_post

import json
router = APIRouter()


@router.post("/create/", status_code=status.HTTP_201_CREATED)
async def create_post(
    title: str = Form(...),
    description: Optional[str] = Form(None),
    communities_id: UUID = Form(...),
    topic_ids: str = Form(
        default="[]",
        description="JSON-строка списка идентификаторов тем. Пример: '[\"uuid1\", \"uuid2\"]'"),
    image: Optional[UploadFile] = File(None),
    current_user=Depends(get_current_users),
    service_post: ServicePost = Depends(get_service_post)
):
    post= await service_post.create()

    print(f"Title: {title}")
    print(f"Topic IDs: {topic_ids}")
    print(f"Image: {image.filename if image else None}")
    return {"message": "Пост создан"}
