from fastapi import APIRouter
from src.services.generate_embeddings import GenerateEmbeddings
from pydantic import BaseModel
from typing import Dict, Any
from src.schema.embeddings_schema import EmbeddingsRequest, EmbeddingsResult



async def embed_text(text: EmbeddingsRequest) -> EmbeddingsResult:
    embeddings = GenerateEmbeddings(text=text.text).generate_embeddings()
    return EmbeddingsResult(result=embeddings)
