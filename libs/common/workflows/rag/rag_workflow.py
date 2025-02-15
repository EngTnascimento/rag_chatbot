from typing import Any
from libs.common.llm_providers.traits import LLMProviderTrait

class RAGWorkflow:
    """Abstract base class defining the interface for RAG (Retrieval Augmented Generation) workflows."""

    def __init__(self, llm_provider: LLMProviderTrait):
        self.llm_provider = llm_provider

    async def execute(self, query: str) -> Any:
        """
        Execute the RAG workflow for a given query.

        Args:
            query (str): The input query to process through the RAG workflow

        Returns:
            Any: The result of the RAG workflow execution
        """
        pass
