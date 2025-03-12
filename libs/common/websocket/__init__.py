from .connection import ConnectionManager
from .schemas import (
    TextMessage,
    WebSocketMessage,
    ChatMessage,
    ChatHistoryMessage,
    ErrorMessage,
    MessageRequest,
    ResponseMessage,
)

# Create a default instance for global use
manager = ConnectionManager()

__all__ = [
    "ConnectionManager",
    "TextMessage",
    "WebSocketMessage",
    "ChatMessage",
    "ChatHistoryMessage",
    "ErrorMessage",
    "MessageRequest",
    "ResponseMessage",
    "manager",
]
