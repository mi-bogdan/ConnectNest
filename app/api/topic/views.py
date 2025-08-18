from fastapi import APIRouter, status, Depends, HTTPException
from .schemas import CreateTopic, ResponseTopic
from typing import Annotated
from app.api.auth.service import get_current_users
from .service import get_service_topic, TopicService
from app.exceptions import PermissionsError, UniqueError, DatabaseException


router = APIRouter()


@router.post("/create/", status_code=status.HTTP_201_CREATED, response_model=ResponseTopic)
async def create_topic(body: CreateTopic, current_user=Depends(get_current_users), services_topic: TopicService = Depends(get_service_topic)):
    try:
        topic = await services_topic.create_topic(body.title, current_user)
        return topic
    except PermissionsError as e:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail=str(e))
    except UniqueError as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail=str(e))
    except DatabaseException as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Внутреняя ошибка сервера")
