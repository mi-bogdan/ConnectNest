from fastapi import FastAPI
import uvicorn
from app.config import settings
from app.api import router as api_router

app = FastAPI(title="ConnectNest")
app.include_router(api_router)

if __name__ == "__main__":
    uvicorn.run("app.main:app", host=settings.app_host, port=settings.app_port)
