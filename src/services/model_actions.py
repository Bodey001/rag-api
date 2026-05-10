from typing import Dict, Any
import requests
from config.settings import Settings
from pydantic import BaseModel


class ModelActions(BaseModel):
    embedding_url: str = Settings().EMBEDDING_URL
    embedding_model: str = Settings().EMBEDDING_MODEL

    generation_url: str = Settings().GENERATION_URL
    generation_model: str = Settings().GENERATION_MODEL


    async def generate_embeddings(self, embedding_text: str) -> Any:
        response = requests.post(f"{self.embedding_url}/api/embed", json={"model": self.embedding_model, "input": embedding_text})
        return response.json()

    async def generate_response(self, generation_text: str) -> Any:
        response = requests.post(f"{self.generation_url}/api/generate", json={"model": self.generation_model, "prompt": generation_text, "stream": False})
        return response.json()["response"]
