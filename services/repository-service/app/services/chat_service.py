from app.services.embedding_service import EmbeddingService
from app.services.qdrant_service import QdrantService
from app.clients.ollama_client import OllamaClient


class ChatService:

    def __init__(self):

        self.embedding = EmbeddingService()
        self.qdrant = QdrantService()
        self.ollama = OllamaClient()

    def chat(
        self,
        repository_id: int,
        question: str,
    ):

        # Generate embedding for the question
        query_vector = self.embedding.embed_query(question)

        # Search similar code chunks
        results = self.qdrant.search_repository(
            repository_id=repository_id,
            vector=query_vector,
            limit=5,
        )

        context = "\n\n".join(
            [
                hit.payload.get("content", "")
                for hit in results
            ]
        )

        prompt = f"""
You are an expert software engineer.

Repository Context:

{context}

Question:

{question}

Answer clearly with references to the repository context.
"""

        return self.ollama.generate(prompt)