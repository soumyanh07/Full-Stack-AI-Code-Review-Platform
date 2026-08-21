from __future__ import annotations

from functools import lru_cache

from sentence_transformers import SentenceTransformer

from app.core.config import settings


@lru_cache(maxsize=1)
def get_embedding_model() -> SentenceTransformer:
    """
    Load the embedding model only once per process.
    """
    print(
        f"Loading embedding model: "
        f"{settings.EMBEDDING_MODEL}"
    )

    return SentenceTransformer(
        settings.EMBEDDING_MODEL
    )


class EmbeddingService:
    """
    Generates embeddings using the configured
    SentenceTransformer model.
    """

    def __init__(self):
        self.model = get_embedding_model()

    def embed(
        self,
        text: str,
    ) -> list[float]:

        vector = self.model.encode(
            text,
            normalize_embeddings=True,
        )

        return vector.tolist()

    def embed_batch(
        self,
        texts: list[str],
    ) -> list[list[float]]:

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

        vector = self.model.encode(
            query,
            normalize_embeddings=True,
        )

        return vector.tolist()