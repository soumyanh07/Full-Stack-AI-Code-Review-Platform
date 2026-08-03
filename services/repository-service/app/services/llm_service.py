import ollama


class LLMService:
    MODEL = "qwen2.5-coder:7b"

    def review(self, prompt: str) -> str:
        response = ollama.chat(
            model=self.MODEL,
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a senior software engineer. "
                        "Review the provided source code. "
                        "Identify bugs, security issues, performance problems, "
                        "clean code improvements, and best practices."
                    ),
                },
                {
                    "role": "user",
                    "content": prompt,
                },
            ],
        )

        return response["message"]["content"]