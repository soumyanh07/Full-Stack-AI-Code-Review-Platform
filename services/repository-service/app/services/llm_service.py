import httpx

from app.core.config import settings



class LLMService:
    """
    Wrapper around local LLM.

    Default:
    Ollama + Qwen2.5-Coder
    """



    def __init__(self):

        self.base_url = (
            settings.OLLAMA_URL
        )

        self.model = (
            settings.LLM_MODEL
        )



    async def generate(
        self,
        prompt: str
    ) -> str:


        payload = {

            "model": self.model,

            "prompt": prompt,

            "stream": False

        }


        async with httpx.AsyncClient(
            timeout=120
        ) as client:


            response = await client.post(

                f"{self.base_url}/api/generate",

                json=payload

            )


            response.raise_for_status()


            data = response.json()



        return data.get(
            "response",
            ""
        )



    async def chat(
        self,
        messages: list
    ):


        payload = {

            "model": self.model,

            "messages": messages,

            "stream": False

        }


        async with httpx.AsyncClient(
            timeout=120
        ) as client:


            response = await client.post(

                f"{self.base_url}/api/chat",

                json=payload

            )


            response.raise_for_status()


            data = response.json()



        return data["message"]["content"]



    async def review_code(
        self,
        code: str
    ):


        prompt = f"""

You are an expert software engineer.

Review this code:

{code}


Find:

- Bugs
- Security vulnerabilities
- Performance issues
- Code quality problems


Return structured JSON.
"""


        return await self.generate(
            prompt
        )