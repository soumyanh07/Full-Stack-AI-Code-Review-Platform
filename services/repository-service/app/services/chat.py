from __future__ import annotations

from app.services.embedding_service import EmbeddingService
from app.services.llm_service import LLMService
from app.services.qdrant_service import QdrantService


class ChatService:
    """
    Repository-aware AI chat service.

    Uses:
        Question
            ↓
        Embedding
            ↓
        Qdrant semantic search
            ↓
        Repository context
            ↓
        Ollama LLM
            ↓
        Answer
    """

    def __init__(self):
        self.embedding = EmbeddingService()
        self.qdrant = QdrantService()
        self.llm = LLMService()

    def chat(
        self,
        repository_id: int,
        question: str,
    ) -> dict:
        """
        Answer a question using repository context.
        """

        # -------------------------------------------------
        # Step 1: Convert the question into an embedding
        # -------------------------------------------------
        query_vector = self.embedding.embed_query(
            question
        )

        # -------------------------------------------------
        # Step 2: Search the repository in Qdrant
        # -------------------------------------------------
        results = self.qdrant.search_repository(
            repository_id=repository_id,
            vector=query_vector,
            limit=5,
        )

        # -------------------------------------------------
        # Step 3: Build context from retrieved chunks
        # -------------------------------------------------
        context_parts = []

        for result in results:
            payload = result.payload or {}

            filename = payload.get(
                "filename",
                "unknown",
            )

            path = payload.get(
                "path",
                "",
            )

            content = payload.get(
                "content",
                "",
            )

            context_parts.append(
                f"File: {filename}\n"
                f"Path: {path}\n"
                f"Content:\n{content}"
            )

        context = "\n\n---\n\n".join(
            context_parts
        )

        # -------------------------------------------------
        # Step 4: Handle repository with no indexed data
        # -------------------------------------------------
        if not context:
            return {
                "repository_id": repository_id,
                "question": question,
                "answer": (
                    "I could not find any indexed code "
                    "for this repository. Please index "
                    "the repository before asking questions."
                ),
                "context": "",
            }

        # -------------------------------------------------
        # Step 5: Build the RAG prompt
        # -------------------------------------------------
        prompt = f"""
You are an AI coding assistant helping a developer
understand a software repository.

Answer the user's question using ONLY the repository
context provided below.

If the answer cannot be determined from the provided
context, clearly say that the available repository
context does not contain enough information.

Do not invent files, functions, classes, APIs, or
implementation details that are not present in the
context.

Repository context:

{context}

User question:

{question}

Provide a clear and technically accurate answer.
""".strip()

        # -------------------------------------------------
        # Step 6: Ask Ollama
        # -------------------------------------------------
        answer = self.llm.generate(
            prompt=prompt
        )

        # -------------------------------------------------
        # Step 7: Return structured response
        # -------------------------------------------------
        return {
            "repository_id": repository_id,
            "question": question,
            "answer": answer,
            "context": context,
        }