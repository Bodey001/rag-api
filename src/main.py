from fastapi import FastAPI
import logging
from src.router.uploads_router import router as uploads_router
from src.router.inference_router import router as inference_router
from config.database import get_db_connection, init_db
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)

app = FastAPI()
logger = logging.getLogger(__name__)
app.include_router(uploads_router, prefix="/api/v1")
app.include_router(inference_router, prefix="/api/v1")


@app.on_event("startup")
async def startup_event():
    logger.info("Starting application")
    init_db()
    logger.info("Server is running on http://localhost:8000")

@app.on_event("shutdown")
async def shutdown_event():
    logger.info("Stopping application")
    get_db_connection().close()
    logger.info("Database connection closed")
