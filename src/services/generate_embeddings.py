from typing import Dict, Any
import requests
from config.settings import Settings
from pydantic import BaseModel


class GenerateEmbeddings(BaseModel):
    host: str = Settings().EMBEDDING_URL
    model: str = Settings().EMBEDDING_MODEL
    text: str

    def generate_embeddings(self) -> Any:
        response = requests.post(f"{self.host}/api/embed", json={"model": self.model, "input": self.text})
        return response.json()
