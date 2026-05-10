DROP INDEX IF EXISTS documents_metadata_idx;
DROP INDEX IF EXISTS chunks_embeddings_idx;
DROP INDEX IF EXISTS chunks_document_id_idx;

DROP TABLE IF EXISTS chunks;
DROP TABLE IF EXISTS documents;

DROP EXTENSION IF EXISTS vector;
