from __future__ import annotations

from typing import List


class ChunkingService:
    """
    Splits source code into overlapping chunks for embedding.
    """

    def __init__(
        self,
        chunk_size: int = 1200,
        overlap: int = 200,
    ):
        self.chunk_size = chunk_size
        self.overlap = overlap

    def chunk(
        self,
        text: str,
    ) -> List[str]:

        if not text:
            return []

        chunks = []

        start = 0

        while start < len(text):

            end = start + self.chunk_size

            chunks.append(text[start:end])

            start += self.chunk_size - self.overlap

        return chunks

    def chunk_document(
        self,
        document: dict,
    ) -> list[dict]:

        chunks = self.chunk(
            document["content"],
        )

        output = []

        for index, chunk in enumerate(chunks):

            output.append(
                {
                    "chunk_id": index,
                    "filename": document["filename"],
                    "language": document["language"],
                    "path": document["path"],
                    "content": chunk,
                }
            )

        return output