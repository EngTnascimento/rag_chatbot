from abc import ABC, abstractmethod
from typing import List, Dict


class LLMProviderTrait(ABC):
    """Abstract base class defining the interface for LLM providers."""

    @abstractmethod
    async def generate(self, prompt: str) -> str:
        """
        Generate a response from the model given a prompt.

        Args:
            prompt (str): The input prompt to send to the model

        Returns:
            str: The generated response
        """
        pass

    @abstractmethod
    async def chat(self, messages: List[Dict[str, str]]) -> str:
        """
        Have a conversation with the model using a list of messages.

        Args:
            messages (List[Dict[str, str]]): List of message dictionaries with 'role' and 'content'

        Returns:
            str: The model's response
        """
        pass
