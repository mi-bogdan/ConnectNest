import time
import logging
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response


class LoggingMiddleware(BaseHTTPMiddleware):
    """Middleware для логирование каждого запроса"""

    def __init__(self, app):
        super().__init__(app)
        self.logger = logging.getLogger(self.__class__.__name__)

    async def dispatch(self, request: Request, call_next):
        start_time = time.time()

        self.logger.info(
            "Входящий запрос",
            extra={
                "method": request.method,
                "path": request.url.path,
                "client_host": request.client.host,
                "headers": dict(request.headers)
            }
        )

        try:
            response: Response = await call_next(request)
        except Exception as e:
            self.logger.error(
                "Ошибка при выполнение запроса",
                extra={
                    "method": request.method,
                    "path": request.url.path,
                    "error": str(e)
                },
                exc_info=True
            )
            raise

        process_time = time.time() - start_time

        self.logger.info(
            "Outgoing Response",
            extra={
                "method": request.method,
                "path": request.url.path,
                "status_code": response.status_code,
                "process_time": f"{process_time:.4f} sec"
            }
        )

        return response
    

class CORSMiddleware:
    pass
