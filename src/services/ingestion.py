# inputs documents and chunks them into smaller pieces no langchain

import docx2txt
import textract
from PyPDF2 import PdfReader


from typing import List
from pydantic import BaseModel

chunk_size = 1000

class Ingestion(BaseModel):
    file_path: str

    def ingest_document(self) -> str:
        if self.file_path.endswith('.pdf'):
            with open(self.file_path, 'rb') as file:
                reader = PdfReader(file.read())
                text = ''
                for page in reader.pages:
                    text += page.extract_text()
        elif self.file_path.endswith('.docx'):
            text = docx2txt.process(self.file_path)
        elif self.file_path.endswith('.doc'):
            text = textract.process(self.file_path)
        return text.decode('utf-8')


    # chunk the entire text into smaller pieces based on the chunk_size
        # dynamically chunk the text into smaller pieces based on the length of the text
    def chunk_text(self) -> List[str]:
        text = self.ingest_document()
        chunks = []
        for i in range(0, len(text), chunk_size):
            chunks.append(text[i:i+chunk_size])
        return chunks
