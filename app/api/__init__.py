from fastapi import APIRouter
from fastapi import Depends

from app.api.auth.views import router as user_router
from app.api.communities.views import router as communities_router
from app.api.auth.service import http_bearer


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
