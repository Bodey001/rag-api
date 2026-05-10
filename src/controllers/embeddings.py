from fastapi import APIRouter
from src.services.model_actions import ModelActions
from pydantic import BaseModel
from typing import Dict, Any
from src.schema.embeddings_schema import EmbeddingsRequest, EmbeddingsResult



async def embed_text(text: EmbeddingsRequest) -> EmbeddingsResult:
    embeddings = await ModelActions().generate_embeddings(embedding_text=text.text)
    return EmbeddingsResult(result=embeddings)
