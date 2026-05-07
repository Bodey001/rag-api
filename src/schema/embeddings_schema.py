from pydantic import BaseModel
from typing import Any


class EmbeddingsRequest(BaseModel):
    text: str

class EmbeddingsResult(BaseModel):
    result: Any
