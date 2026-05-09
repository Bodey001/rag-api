from pydantic import BaseModel, ConfigDict
from typing import Any, List, Optional
from datetime import datetime

class DocumentSchema(BaseModel):
    id: Optional[int] = None
    title: str
    metadata: Any
    chunk_count: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

class MetadataSchema(BaseModel):
    author: Optional[str] = None
    title: Optional[str] = None
    year: Optional[str] = None
    source_url: Optional[str] = None
    tags: Optional[List[str]] = []

    model_config = ConfigDict(extra="allow")

class ChunkSchema(BaseModel):
    id: Optional[int] = None
    document_id: int
    chunk_index: int
    content: str
    embeddings: List[float]
    embedding_model: str
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
