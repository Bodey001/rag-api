# Allows the uploading of files to the llm

from fastapi import UploadFile, File
from typing import Dict
from src.services.ingestion import Ingestion
from src.services.generate_embeddings import GenerateEmbeddings



async def upload_file(file: UploadFile = File(...)) -> Dict[str, str]:
    embeddings = []
    ingestion = Ingestion(file.file)
    text = ingestion.ingest_document()
    chunks = ingestion.chunk_text()

    for chunk in chunks:
        embeddings.append(GenerateEmbeddings(text=chunk).generate_embeddings())

    return {"result": embeddings}
