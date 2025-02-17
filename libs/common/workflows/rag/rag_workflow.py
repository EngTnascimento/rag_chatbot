from typing import Any
from langgraph.graph import StateGraph
from libs.common.llm_providers.traits import LLMProviderTrait
from libs.common.workflows.traits.workflow_trait import WorkflowTrait
from libs.common.workflows.rag import RAGState


class RAGWorkflow(WorkflowTrait):
    """Abstract base class defining the interface for RAG (Retrieval Augmented Generation) workflows."""

    def __init__(self, llm_provider: LLMProviderTrait):
        self.llm_provider = llm_provider
        self.rag_builder = StateGraph(RAGState)

    async def execute(self, state: RAGState) -> Any:
        """
        Execute the RAG workflow for a given query.

        Args:
            query (str): The input query to process through the RAG workflow

        Returns:
            Any: The result of the RAG workflow execution
        """
        pass
