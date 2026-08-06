from __future__ import annotations

from sentence_transformers import SentenceTransformer

from app.core.config import settings


class EmbeddingService:
    """
    Generates embeddings using the configured SentenceTransformer model.
    """

    def __init__(self):
        self.model = SentenceTransformer(
            settings.EMBEDDING_MODEL
        )

    def embed(
        self,
        text: str,
    ) -> list[float]:
        """
        Generate embedding for a single text.
        """
        vector = self.model.encode(
            text,
            normalize_embeddings=True,
        )

        return vector.tolist()

    def embed_batch(
        self,
        texts: list[str],
    ) -> list[list[float]]:
        """
        Generate embeddings for multiple texts.
        """
        vectors = self.model.encode(
            texts,
            normalize_embeddings=True,
            batch_size=32,
            show_progress_bar=False,
        )

        return vectors.tolist()

    def embed_query(
        self,
        query: str,
    ) -> list[float]:
        """
        Generate embedding for a user query.
        """
        vector = self.model.encode(
            query,
            normalize_embeddings=True,
        )

        return vector.tolist()