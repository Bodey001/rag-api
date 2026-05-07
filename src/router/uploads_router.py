from fastapi import APIRouter, Body
from src.controllers.uploads_controller import upload_file
from src.controllers.embeddings import embed_text
from src.schema.embeddings_schema import EmbeddingsRequest, EmbeddingsResult
from typing import Dict, Any


router = APIRouter()

router.post("/upload")(upload_file)

router.get("/")(lambda: {"message": "Welcome to the RAG API"})


@router.post("/embed")
async def embed_endpoint(text: EmbeddingsRequest = Body(...)) -> EmbeddingsResult:
    return await embed_text(text)
