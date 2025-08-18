from fastapi import APIRouter
from fastapi import Depends

from app.api.auth.views import router as user_router
from app.api.communities.views import router as communities_router
from app.api.auth.service import http_bearer
from app.api.topic.views import router as topic_router
from app.api.post.views import router as post_router


router = APIRouter()

router.include_router(
    router=user_router,
    prefix="/auth",
    tags=["auth"],
    dependencies=[Depends(http_bearer)]
)

router.include_router(
    router=communities_router,
    prefix="/communities",
    tags=["communities"]
)

router.include_router(
    router=topic_router,
    prefix="/topic",
    tags=["topic"]
)

router.include_router(
    router=post_router,
    prefix="/post",
    tags=["post"]
)
