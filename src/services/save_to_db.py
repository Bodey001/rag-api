from config.database import get_db_connection
from src.schema.documents_schema import DocumentSchema, ChunkSchema, MetadataSchema
from typing import List
import logging

logger = logging.getLogger(__name__)



# Save a document to the database and return the document id
async def save_document_to_db(document_schema: DocumentSchema, metadata: MetadataSchema) -> int:
    try:
        conn = get_db_connection()
        with conn.cursor() as cur:
            logger.info(f"Performing insert operation for document: {document_schema.title} to database")
            cur.execute("INSERT INTO documents (title, chunk_count, metadata) VALUES (%s, %s, %s) RETURNING id", (document_schema.title, document_schema.chunk_count, metadata.model_dump_json()))

            logger.info(f"Fetching document id for document: {document_schema.title}")
            document_id = cur.fetchone()[0]
            logger.info(f"Document inserted successfully: {document_schema.title}, id: {document_id}")

            conn.commit()

            return document_id
    except Exception as e:
        conn.rollback()
        logger.error(f"Error saving document to database: {e}")
        raise

# Save a batch of chunks to the database
async def save_chunks_to_db(chunk_schemas: List[ChunkSchema]) -> None:
    try:
        conn = get_db_connection()
        with conn.cursor() as cur:
            cur.executemany("INSERT INTO chunks (document_id, chunk_index, content, embeddings, embedding_model) VALUES (%s, %s, %s, %s, %s)", [(chunk_schema.document_id, chunk_schema.chunk_index, chunk_schema.content, chunk_schema.embeddings, chunk_schema.embedding_model) for chunk_schema in chunk_schemas])
            conn.commit()
    except Exception as e:
        conn.rollback()
        logger.error(f"Error saving chunk to database: {e}")
        raise
