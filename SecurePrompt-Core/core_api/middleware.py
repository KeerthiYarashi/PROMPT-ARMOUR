import logging
import time
from pathlib import Path
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from slowapi import Limiter
from slowapi.util import get_remote_address

# Setup logs directory
LOGS_DIR = Path(__file__).resolve().parent.parent / "logs"
LOGS_DIR.mkdir(exist_ok=True)

# Define logger
logger = logging.getLogger("api_request_logger")
logger.setLevel(logging.INFO)
file_handler = logging.FileHandler(LOGS_DIR / "api_requests.log")
file_handler.setFormatter(logging.Formatter("%(asctime)s - %(message)s"))
logger.addHandler(file_handler)

# Rate limiter setup
limiter = Limiter(key_func=get_remote_address)

class LoggingAndLengthMiddleware(BaseHTTPMiddleware):
    """
    Middleware to handle:
    1. Blocking requests with prompt lengths > 2000 characters early.
    2. Logging the method, path, IP, and execution time to a log file.
    """
    async def dispatch(self, request: Request, call_next):
        
        # Fast length block based on strict limit
        if request.headers.get("content-length"):
            length = int(request.headers.get("content-length", 0))
            if length > 5000: # Setting 5k bytes limit considering json structure
                return Response(
                    content='{"error": "Payload too large"}', 
                    status_code=413, 
                    media_type="application/json"
                )

        start_time = time.time()
        try:
            response = await call_next(request)
        except Exception as e:
            raise e
        finally:
            process_time = time.time() - start_time
            client_ip = request.client.host if request.client else "Unknown"
            logger.info(f"{request.method} {request.url.path} - IP: {client_ip} - Time: {process_time:.4f}s")
        
        return response