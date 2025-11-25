
import os
from langchain_openai import ChatOpenAI


class OpenaiClient:

    def __init__(self) -> None:
        self.model_name = self._get_model_name()
        self.llm = ChatOpenAI(model=self.model_name)

    def _get_model_name(self) -> str:
        llm_name = os.getenv("OPENAI_MODEL_NAME")
        if not llm_name:
            raise RuntimeError("Environment variable 'OPENAI_MODEL_NAME' is not set.")
        return llm_name

    async def generate(self, prompt: str) -> None:
        """Send a prompt to the model and return its response."""
        response = await self.llm.ainvoke(prompt)
        print(response)
