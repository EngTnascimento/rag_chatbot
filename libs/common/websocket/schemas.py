from pydantic import BaseModel, Field
from typing import Literal, Dict, List, Union
from datetime import datetime
import uuid


class TextMessage(BaseModel):
    """A simple text message"""

    content: str
    role: Literal["user", "assistant"]


class WebSocketMessage(BaseModel):
    """Base class for all websocket messages"""

    message_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    timestamp: datetime = Field(default_factory=datetime.now)
    type: str


class ChatMessage(WebSocketMessage):
    """Message containing chat content"""

    type: Literal["chat"] = "chat"
    data: TextMessage


class ChatHistoryMessage(WebSocketMessage):
    """Message containing chat history"""

    type: Literal["history"] = "history"
    data: List[TextMessage]


class ErrorMessage(WebSocketMessage):
    """Error message"""

    type: Literal["error"] = "error"
    data: Dict[str, str]


class MessageRequest(BaseModel):
    """Client request with text message"""

    text: str
    user_id: str = ""
    session_id: str = ""


# Type for sending messages to client
ResponseMessage = Union[ChatMessage, ChatHistoryMessage, ErrorMessage]
