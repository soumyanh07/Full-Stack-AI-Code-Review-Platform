from app.services.embedding_service import EmbeddingService
from app.services.qdrant_service import QdrantService
from app.services.llm_service import LLMService


class ChatService:

    def __init__(self):
        self.embedding = EmbeddingService()
        self.qdrant = QdrantService()
        self.llm = LLMService()

    def chat(
        self,
        repository_id: int,
        question: str,
    ):
        question_embedding = self.embedding.generate_embedding(
            question
        )

        results = self.qdrant.search(
            question_embedding,
            limit=5,
        )

        context = []
        

        for point in results:
            payload = point.payload

            if payload.get("repository_id") == repository_id:
                context.append(payload["text"])

        prompt = f"""
You are a senior software engineer.

Answer ONLY using the repository context below.

If the answer is not present in the context, say:

"I couldn't find that information in this repository."

Repository Context:

{chr(10).join(context)}

Question:

{question}
"""

        return self.llm.review(prompt)