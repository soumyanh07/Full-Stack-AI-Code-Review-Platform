from __future__ import annotations

from app.services.rag_service import RAGService
from app.services.llm_service import LLMService


class ChatService:
    """
    Repository-aware AI chat service.

    Flow:
        Question
            ?
        Embedding
            ?
        Semantic search
            ?
        Repository context
            ?
        Ollama LLM
            ?
        Answer
    """

    def __init__(self):
        self.rag = RAGService()
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
        # Step 1: Retrieve relevant repository context
        # -------------------------------------------------

        context = self.rag.build_context(
            repository_id=repository_id,
            query=question,
            limit=5,
        )

        # -------------------------------------------------
        # Step 2: Handle missing repository context
        # -------------------------------------------------

        if context == "NO_RELEVANT_CONTEXT_FOUND":
            return {
                "repository_id": repository_id,
                "question": question,
                "answer": (
                    "I could not find any relevant indexed code "
                    "for this repository. Please index the repository "
                    "before asking questions."
                ),
                "context": context,
            }

        # -------------------------------------------------
        # Step 3: Build RAG prompt
        # -------------------------------------------------

        prompt = f"""
You are an AI coding assistant helping a developer
understand a software repository.

Answer the user's question using ONLY the repository
context provided below.

Rules:
- Do not invent files, functions, classes, APIs, or implementation details.
- Mention the relevant file paths when explaining the answer.
- If the context is insufficient, clearly say so.
- Prefer explaining the actual implementation over generic framework knowledge.
- Keep the answer concise but technically accurate.

Repository context:

{context}

User question:

{question}

Provide a clear and technically accurate answer.
""".strip()

        # -------------------------------------------------
        # Step 4: Ask Ollama
        # -------------------------------------------------

        answer = self.llm.generate(
            prompt=prompt
        )

        # -------------------------------------------------
        # Step 5: Return structured response
        # -------------------------------------------------

        return {
            "repository_id": repository_id,
            "question": question,
            "answer": answer,
            "context": context,
        }
