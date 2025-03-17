from typing import Annotated
from langgraph.graph.message import add_messages
from typing_extensions import TypedDict


class RAGState(TypedDict):
    documents: Annotated[list, lambda docs, new_docs: docs + new_docs]
    messages: Annotated[list, add_messages]
    prompt_template: Annotated[str, lambda _, new: new]
    query: Annotated[str, lambda _, new: new]
    query_result: Annotated[str, lambda _, new: new]
