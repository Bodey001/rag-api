# Allows the uploading of files to the llm

from fastapi import UploadFile
from typing import Dict
from src.services.doc_actions import DocActions
from src.services.model_actions import ModelActions
from src.schema.documents_schema import DocumentSchema, ChunkSchema
from src.services.db_actions import DbActions
import logging

logger = logging.getLogger(__name__)


async def upload_file(file: UploadFile) -> Dict[str, str]:

    try:
        logger.info(f"Ingesting document: {file.filename}")
        text, metadata = await DocActions().ingest_document(file)

        if text is None:
            return {"message": "Error ingesting document"}

        chunks = await DocActions().chunk_text(text)
        chunk_count = len(chunks)
        logger.info(f"Chunks created: {chunk_count}")
    except Exception as e:
        logger.error(f"Error ingesting document: {e}")
        return {"message": f"Error ingesting document: {e}"}

    # Save document to database
    try:
        logger.info(f"Saving document to database: {file.filename}")
        document = DocumentSchema(title=file.filename, chunk_count=chunk_count, metadata=metadata)
        document_id = await DbActions().save_document_to_db(document, metadata)
        logger.info(f"Document saved successfully: {file.filename}, id: {document_id}")
    except Exception as e:
        logger.error(f"Error saving document to database: {e}")
        return {"message": f"Error saving document to database: {e}"}

    if document_id is None:
        return {"message": "Error saving document to database"}

    try:
        logger.info(f"Generating embeddings for {chunk_count} chunks")
        chunks_batch = []

        for index, chunk in enumerate(chunks):
            embeddings_response = await ModelActions().generate_embeddings(embedding_text=chunk)

            chunk_schema = ChunkSchema(
                document_id=document_id,
                chunk_index=index,
                content=chunk,
                embeddings=embeddings_response['embeddings'][0],
                embedding_model=embeddings_response['model']
            )
            chunks_batch.append(chunk_schema)

        logger.info(f"Saving {len(chunks_batch)} chunks to database")
        await DbActions().save_chunks_to_db(chunks_batch)
        logger.info(f"Chunks saved successfully: {file.filename}")
    except Exception as e:
        logger.error(f"Error saving chunks to database: {e}")
        return {"message": f"Error saving chunks to database: {e}"}


    logger.info("File Saved Successfully")
    return {"message": "File uploaded successfully"}
