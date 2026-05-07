from fastapi import FastAPI
import logging
from src.router.uploads_router import router as uploads_router

app = FastAPI()
logger = logging.getLogger(__name__)
app.include_router(uploads_router, prefix="/api/v1")

logger.info("Application started")
logger.info("Server is running on http://localhost:8000")
