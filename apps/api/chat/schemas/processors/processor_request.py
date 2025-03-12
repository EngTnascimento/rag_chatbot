from pydantic import BaseModel, Field


class ProcessorRequest(BaseModel):
    """Request schema for text splitting and ChromaDB ingestion processor"""

    key: str = Field(..., description="Key of the file to be processed")
