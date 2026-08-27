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
        Ollama LLM
              ↓
        AI Answer
    """

    # Keep the prompt small for local LLM performance.
    MAX_CONTEXT_CHARS = 3500

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
        Answer a repository question using RAG + local LLM.
        """

        # ---------------------------------------------
        # Step 1: Retrieve repository context
        # ---------------------------------------------

        context = self.rag_service.build_context(
            repository_id=repository_id,
            query=question,
            limit=limit,
        )

        # ---------------------------------------------
        # Step 2: No relevant context
        # ---------------------------------------------

        if context == "NO_RELEVANT_CONTEXT_FOUND":
            return {
                "answer": (
                    "I couldn't find enough information "
                    "in the indexed repository."
                ),
                "context": "",
                "question": question,
                "repository_id": repository_id,
            }

        # ---------------------------------------------
        # Step 3: Limit context size
        # ---------------------------------------------

        if len(context) > self.MAX_CONTEXT_CHARS:
            context = context[: self.MAX_CONTEXT_CHARS]

        # ---------------------------------------------
        # Step 4: Build concise grounded prompt
        # ---------------------------------------------

        prompt = f"""
You are an AI assistant for a software repository.

Answer the user's question using ONLY the repository
context provided below.

Rules:
- Use information supported by the context.
- You may combine information from multiple files.
- Do not invent files, classes, functions, dependencies,
  or behavior.
- Mention file paths when supported by the context.
- For architecture questions, summarize how the retrieved
  components relate to each other.
- If the context is insufficient, say:
  "I couldn't find enough information in the indexed repository."
- Keep the answer concise and technically useful.

REPOSITORY CONTEXT:
{context}

USER QUESTION:
{question}

ANSWER:
""".strip()

        # ---------------------------------------------
        # Step 5: Generate answer
        # ---------------------------------------------

        answer = self.llm_service.generate(
            prompt=prompt,
            timeout=180,
        )

        # ---------------------------------------------
        # Step 6: Protect against empty LLM responses
        # ---------------------------------------------

        if not answer:
            answer = (
                "I couldn't generate an answer from the "
                "indexed repository."
            )

        # ---------------------------------------------
        # Step 7: Return response
        # ---------------------------------------------

        return {
            "answer": answer,
            "context": context,
            "question": question,
            "repository_id": repository_id,
        }