from pydantic import BaseModel, Field


class OllamaConfig(BaseModel):
    base_url: str = Field(default="http://localhost:11434", description="Base URL for Ollama API")
    model: str = Field(default="llama3.1", description="Default model to use")
    max_tokens: int = Field(default=2048, description="Maximum tokens in response")
    temperature: float = Field(default=0.7, ge=0.0, le=1.0, description="Controls randomness")
    top_p: float = Field(default=0.9, ge=0.0, le=1.0, description="Nucleus sampling parameter")
    top_k: int = Field(default=40, ge=1, description="Top-k sampling parameter")

    class Config:
        frozen = True


ollama_config = OllamaConfig(
    temperature=0.0,
    model="llama3.1",
)


