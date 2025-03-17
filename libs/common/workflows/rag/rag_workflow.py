from langgraph.graph import StateGraph, START, END
from libs.common.workflows.rag.rag_state import RAGState
from langgraph.checkpoint.memory import MemorySaver
from .nodes.retriever_node import retriever_node
from .nodes.generate_node import generate_node
from .nodes.pandas_generator_node import pandas_generator_node
from libs.common.llm_providers.openai.services.openai_service import OpenaiService
import pandas as pd


class RAGWorkflow:
    """Abstract base class defining the interface for RAG (Retrieval Augmented Generation) workflows."""

    def __init__(self, llm_provider: OpenaiService):
        self.llm_provider = llm_provider
        self.builder = StateGraph(RAGState)
        self.graph = self._compile()

    def _compile(self) -> StateGraph:
        self.builder.add_node(
            "retrieve",
            retriever_node,
        )
        self.builder.add_node(
            "generate",
            generate_node,
        )
        self.builder.add_node(
            "pandas_generator",
            pandas_generator_node,
        )
        self.builder.add_edge(START, "retrieve")
        self.builder.add_edge("retrieve", "pandas_generator")
        self.builder.add_edge("pandas_generator", "generate")
        self.builder.add_edge("generate", END)
        memory = MemorySaver()
        graph = self.builder.compile(checkpointer=memory)
        return graph

    async def execute(
        self, user_message: str, user_id: str, prompt_template: str
    ) -> str:
        config = {"configurable": {"thread_id": user_id}}
        events = self.graph.stream(
            {
                "messages": [{"role": "user", "content": user_message}],
                "prompt_template": prompt_template,
            },
            config,
            stream_mode="values",
        )
        for event in events:
            message = event["messages"][-1]
            if message.type == "ai":
                return message.content
