from config.database import get_db_connection
from src.schema.documents_schema import DocumentSchema, ChunkSchema, MetadataSchema, ChunkResult
from typing import List
import logging
from pydantic import BaseModel
from src.schema.user_query_schema import QueryEmbeddings
logger = logging.getLogger(__name__)


class DbActions(BaseModel):
# Save a document to the database and return the document id
    async def save_document_to_db(self, document_schema: DocumentSchema, metadata: MetadataSchema) -> int:
        try:
            conn = get_db_connection()
            with conn.cursor() as cur:
                logger.info(f"Performing insert operation for document: {document_schema.title} to database")
                cur.execute("""
                    INSERT INTO documents (title, chunk_count, metadata) VALUES (%s, %s, %s) RETURNING id
                """, (document_schema.title, document_schema.chunk_count, metadata.model_dump_json()))

                logger.info(f"Fetching document id for document: {document_schema.title}")
                document_id = cur.fetchone()[0]
                logger.info(f"Document inserted successfully: {document_schema.title}, id: {document_id}")

                conn.commit()
                return document_id
        except Exception as e:
            conn.rollback()
            logger.error(f"Error saving document to database: {e}")
            return None

    # Save a batch of chunks to the database
    async def save_chunks_to_db(self, chunk_schemas: List[ChunkSchema]) -> None:
        try:
            conn = get_db_connection()
            with conn.cursor() as cur:
                cur.executemany("""
                        INSERT INTO chunks (document_id, chunk_index, content, embeddings, embedding_model)
                        VALUES (%s, %s, %s, %s::vector, %s)
                    """, [(chunk_schema.document_id, chunk_schema.chunk_index, chunk_schema.content, chunk_schema.embeddings, chunk_schema.embedding_model) for chunk_schema in chunk_schemas])
                conn.commit()
        except Exception as e:
            conn.rollback()
            logger.error(f"Error saving chunk to database: {e}")
            return

    # Perform vector similarity search on chunks table
    async def query_chunks_from_db(self, query_embeddings: QueryEmbeddings, limit: int = 5) -> List[ChunkResult]:
        try:
            conn = get_db_connection()
            with conn.cursor() as cur:
                cur.execute("""
                    SELECT document_id, chunk_index, content, embeddings <-> %s::vector AS distance
                    FROM chunks
                    ORDER BY distance
                    LIMIT %s
                """, (query_embeddings.embeddings, limit))
                chunks = cur.fetchall()
            return [
                ChunkResult(
                    document_id=row[0],
                    chunk_index=row[1],
                    content=row[2],
                    distance=row[3]
                )
                for row in chunks
            ]
        except Exception as e:
            logger.error(f"Error querying chunks from database: {e}")
            return []
