from typing import Annotated
from pydantic import BaseModel
from langgraph.graph import StateGraph
from langgraph.graph.message import add_messages

class RAGState(BaseModel):
    documents: Annotated[list, lambda doc: ]
    messages: Annotated[list, add_messages]


# graph_builder = StateGraph(RAGState)
