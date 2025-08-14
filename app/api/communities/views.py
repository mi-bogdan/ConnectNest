
from fastapi import APIRouter, UploadFile, status, HTTPException, Depends, File, Form

from typing import Annotated, Optional, List

from .schemas import CreateCommunities, CommunityAll, CommunityAllAdmin
from .service import get_community_service, CommunityService, ReadCommunotyService, GetCommunityAllAdmin, get_community_all, get_community_all_admin

from app.exceptions import InvalidImageExtension, FileSaveError
from app.core.pagination import PaginationParams, PaginatedResponse
from app.api.auth.service import get_current_users
from app.db.models.user import User
import logging


router = APIRouter()


@router.post("/create_communities/", status_code=status.HTTP_201_CREATED)
async def create_communities(
        title: str = Form(...),
        description: Optional[str] = Form(None),
        image_logo: Optional[UploadFile] = File(None),
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


@router.get("/all_communities/", status_code=status.HTTP_200_OK, response_model=PaginatedResponse[CommunityAll])
async def get_all_communities(params: PaginationParams = Depends(), read_community_service: ReadCommunotyService = Depends(get_community_all)):
    return await read_community_service.get(page=params.page, size=params.size)


@router.get("/admin_all/communities/", status_code=status.HTTP_200_OK, response_model=list[CommunityAllAdmin])
async def get_all_commnities_admin(current_user: Annotated[User, Depends(get_current_users)], services: Annotated[GetCommunityAllAdmin, Depends(get_community_all_admin)]):
    return await services.get(current_user)
