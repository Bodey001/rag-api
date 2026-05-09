from fastapi import APIRouter, Body, UploadFile, File
from src.controllers.uploads_controller import upload_file
from src.controllers.embeddings import embed_text
from src.schema.embeddings_schema import EmbeddingsRequest, EmbeddingsResult
from typing import Dict, Any


router = APIRouter()

router.get("/")(lambda: {"message": "Welcome to the RAG API"})


@router.post("/embed")
async def embed_endpoint(text: EmbeddingsRequest = Body(...)) -> EmbeddingsResult:
    return await embed_text(text)


@router.post("/upload")
async def upload_endpoint(file: UploadFile = File(...)) -> Dict[str, str]:
    return await upload_file(file)
