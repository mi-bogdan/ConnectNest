from fastapi import FastAPI
import uvicorn
from config import settings

app = FastAPI(title="educational-project")


if __name__ == "__main__":
    uvicorn.run(app, host=settings.app_host, port=settings.app_port)
