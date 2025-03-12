from pydantic import BaseModel, Field
from typing import Optional
import chromadb.utils.embedding_functions as embedding_functions


class ChromaConfig(BaseModel):
    collection_name: str = Field(
        default="default", description="Name of the ChromaDB collection"
    )
    embedding_function: Optional[embedding_functions.EmbeddingFunction] = Field(
        description="Embeddings function to use for ChromaDB",
    )

    model_config = {"arbitrary_types_allowed": True}
