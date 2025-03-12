from langchain_openai import ChatOpenAI
from libs.common.llm_providers.openai.config.openai_config import (
    ChatOpenAIConfig,
    OpenAIEmbeddingsConfig,
)
import chromadb.utils.embedding_functions as embedding_functions
import os


class OpenaiService:
    def __init__(
        self,
        chat_config: ChatOpenAIConfig = ChatOpenAIConfig(),
        embeddings_config: OpenAIEmbeddingsConfig = OpenAIEmbeddingsConfig(),
    ):
        self.chat_model = ChatOpenAI(**chat_config.model_dump())
        self.embeddings = embedding_functions.OpenAIEmbeddingFunction(
            api_key=os.getenv("OPENAI_API_KEY"), model_name="text-embedding-3-small"
        )
