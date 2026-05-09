# inputs documents and chunks them into smaller pieces no langchain

from PyPDF2 import PdfReader
from docx import Document as DocxDocument

from typing import List, Optional, Tuple
from pydantic import BaseModel
from fastapi import UploadFile
import logging

from src.schema.documents_schema import MetadataSchema

logger = logging.getLogger(__name__)

chunk_size = 1000


class Ingestion(BaseModel):

    def ingest_document(self, file: UploadFile) -> Tuple[Optional[str], MetadataSchema]:
        try:
            if file.filename.endswith('.pdf'):
                reader = PdfReader(file.file)
                text = ''.join(page.extract_text() or '' for page in reader.pages)
                raw = reader.metadata or {}
                metadata = MetadataSchema(
                    title=raw.title,
                    author=raw.author,
                    year=str(raw.creation_date.year) if getattr(raw, 'creation_date', None) else None,
                )

            elif file.filename.endswith('.docx'):
                doc = DocxDocument(file.file)
                props = doc.core_properties
                text = '\n'.join(p.text for p in doc.paragraphs)
                metadata = MetadataSchema(
                    title=props.title or None,
                    author=props.author or None,
                    year=str(props.created.year) if props.created else None,
                )

            elif file.filename.endswith('.txt'):
                text = file.file.read().decode('utf-8')
                metadata = MetadataSchema(
                    title=file.filename,
                    author=None,
                    year=None,
                )
            else:
                logger.warning(f"Unsupported file type: {file.filename}")
                return None, None

            return text, metadata
        except Exception as e:
            logger.error(f"Error ingesting document: {e}")
            return None, None

    # chunk the text into smaller pieces based on the chunk_size
    def chunk_text(self, text: str) -> List[str]:
        chunks = []
        for i in range(0, len(text), chunk_size):
            chunks.append(text[i:i+chunk_size])
        return chunks
