from fastapi import APIRouter, UploadFile, status, HTTPException, Form
from fastapi.params import Depends

from typing import Annotated, Optional

from .schemas import CreateCommunities
from .service import get_community_service, CommunityService

from app.exceptions import InvalidImageExtension, FileSaveError
import logging

router = APIRouter()


@router.post("/create_communities/", status_code=status.HTTP_201_CREATED)
async def create_communities(
        title: str,
        description: str | None,
        image_logo: UploadFile | None,
        community_service: CommunityService = Depends(get_community_service)
):
    logger = logging.getLogger(__name__)
    logger.info(
        "Запрос на создания сообщества",
        extra={
            "title": title,
            "description": description
        })
    try:
        community_data = CreateCommunities(
            title=title, description=description)
        logger.info("Запрос на создание сообщества выполнен успешно")
        return await community_service.create_community(body=community_data, image_logo=image_logo)
    except InvalidImageExtension as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=str(e))
    except FileSaveError as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=str(e))
