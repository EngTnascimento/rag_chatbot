from pydantic import BaseModel
from typing import Optional, Dict, Any


class ProcessorResponse(BaseModel):
    success: bool = True
    error: Optional[str] = None
