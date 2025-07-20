from fastapi import FastAPI
import uvicorn
import logging
from app.config import settings
from app.api import router as api_router
from app.config.logging import ExtendedConfigLogger
from app.api.middleware.middlewares import LoggingMiddleware

ExtendedConfigLogger.get_log_config()

logger = logging.getLogger(__name__)

app = FastAPI(title="ConnectNest")
app.include_router(api_router)

app.add_middleware(LoggingMiddleware)

logger.info(f"Приложение запущено на {settings.app_host}:{settings.app_port}")

if __name__ == "__main__":
    uvicorn.run("app.main:app", host=settings.app_host, port=settings.app_port)
