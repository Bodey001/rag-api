from pydantic import BaseModel
from typing import List

class UserQuery(BaseModel):
    query: str

class QueryEmbeddings(BaseModel):
    embeddings: List[float]
