from src.services.model_actions import ModelActions
from src.schema.user_query_schema import UserQuery, QueryEmbeddings
from src.services.db_actions import DbActions
from src.services.doc_actions import DocActions
import logging
from fastapi.responses import PlainTextResponse

logger = logging.getLogger(__name__)

async def infer_query(user_query: UserQuery) -> PlainTextResponse:

    # Generate embeddings for the query
    try:
        logger.info(f"Inferring query: {user_query.query}")
        embeddings = await ModelActions().generate_embeddings(embedding_text=user_query.query)
        logger.info("Embeddings generated successfully for user query")

    except Exception as e:
        logger.error(f"Error inferring query: {e}")
        return f"Error inferring query: {e}"

    # Query chunks from database based on query embeddings similarity (Retrieval)
    try:
        logger.info("Querying chunks from database based on query embeddings similarity")
        chunks = await DbActions().query_chunks_from_db(QueryEmbeddings(embeddings=embeddings['embeddings'][0]))
        logger.info("Chunks queried successfully from database")
        print(chunks)

        if len(chunks) == 0:
            return "No chunks found in database"
        content = " ".join([chunk.content for chunk in chunks])
        logger.info("Content retrieved successfully from database")
    except Exception as e:
        logger.error(f"Error querying chunks from database: {e}")
        return f"Error querying chunks from database: {e}"

    # Augment the content with the query
    try:
        logger.info("Augmenting content with the query")
        augmented_content = await DocActions().augment_content(content, user_query.query)
        logger.info("Content augmented successfully")
    except Exception as e:
        logger.error(f"Error augmenting content: {e}")
        return f"Error augmenting content: {e}"

    # Generate response based on retrieved content (Generation)
    try:
        logger.info("Generating response based on retrieved content")
        response = await ModelActions().generate_response(generation_text=augmented_content)

        if len(response) == 0:
            return "No response generated"

        final_response = await DocActions().generate_response(response=response)
        logger.info("Response generated successfully")
    except Exception as e:
        logger.error(f"Error generating response: {e}")
        return f"Error generating response: {e}"

    return final_response
