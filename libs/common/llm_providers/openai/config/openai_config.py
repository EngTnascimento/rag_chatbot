from pydantic import BaseModel, Field
import os


class ChatOpenAIConfig(BaseModel):
    """Configuration settings for OpenAI API."""

    api_key: str | None = Field(
        default=os.getenv("OPENAI_API_KEY"),
        description="OpenAI API key for authentication",
    )
    model_name: str = Field(
        default="gpt-3.5-turbo", description="Name of the OpenAI model to use"
    )
    temperature: float = Field(
        default=0.3,
        ge=0.0,
        le=2.0,
        description="Controls randomness in the model's output. Higher values mean more random completions.",
    )
    max_tokens: int = Field(
        default=2000,
        gt=0,
        description="Maximum number of tokens to generate in the completion",
    )
    timeout: int = Field(
        default=30, gt=0, description="Timeout in seconds for API requests"
    )


class OpenAIEmbeddingsConfig(BaseModel):
    """Configuration settings for OpenAI embeddings."""

    api_key: str | None = Field(
        default=os.getenv("OPENAI_API_KEY"),
        description="OpenAI API key for authentication",
    )
    model: str = Field(
        default="text-embedding-3-small",
        description="Name of the OpenAI embeddings model to use",
    )
