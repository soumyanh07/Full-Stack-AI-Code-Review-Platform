from __future__ import annotations

from app.services.llm_service import LLMService
from app.services.rag_service import RAGService


class ChatService:
    """
    Repository-aware AI chat service.

    Flow:
        User Question
              ↓
        RAGService
              ↓
        Relevant Repository Context
              ↓
        LLMService / Ollama
              ↓
        AI Answer
    """

    def __init__(self):
        self.rag_service = RAGService()
        self.llm_service = LLMService()

    def chat(
        self,
        repository_id: int,
        question: str,
        limit: int = 5,
    ) -> dict:
        """
        Answer a question using repository context retrieved through RAG.
        """

        # Retrieve relevant repository context.
        context = self.rag_service.build_context(
            repository_id=repository_id,
            query=question,
            limit=limit,
        )

        # Build the LLM prompt.
        prompt = f"""
You are an AI software engineering assistant.

Answer the user's question using the repository context provided below.

Rules:

1. Use the repository context as the primary source of truth.
2. Do not invent files, code, or repository details.
3. If the context does not contain enough information, clearly say so.
4. Give a concise but useful answer.
5. When discussing code, explain the relevant file and code behavior.

Repository Context:

{context}

User Question:

{question}

Answer:
""".strip()

        # Generate the answer using Ollama.
        answer = self.llm_service.generate(
            prompt=prompt,
        )

        return {
            "repository_id": repository_id,
            "question": question,
            "context": context,
            "answer": answer,
        }