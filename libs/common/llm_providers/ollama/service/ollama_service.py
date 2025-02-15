from langchain_ollama import OllamaLLM, ChatOllama
from langchain.schema import BaseMessage
from libs.common.llm_providers.ollama.config import ollama_config, OllamaConfig
from libs.common.llm_providers.traits import LLMProviderTrait

class OllamaService(LLMProviderTrait):
    def __init__(self, config: OllamaConfig = ollama_config):
        self.config = config
        self.chat_model = ChatOllama(**config.model_dump())
        self.completion_model = OllamaLLM(**config.model_dump())

    async def generate(self, prompt: str) -> str:
        """
        Generate a response from the Ollama model.
        
        Args:
            prompt (str): The input prompt to send to the model
            
        Returns:
            str: The generated response
        """
        response: BaseMessage = await self.chat_model.ainvoke(prompt)
        return str(response.content)

    async def chat(self, messages: list[dict]) -> str:
        """
        Have a conversation with the Ollama model.
        
        Args:
            messages (list[dict]): List of message dictionaries with 'role' and 'content'
            
        Returns:
            str: The model's response
        """
        response: str = await self.completion_model.ainvoke(messages)
        return response

