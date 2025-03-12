from libs.common.workflows.rag.rag_state import RAGState
from libs.common.database.chromadb.chroma_service import ChromaService
from libs.common.workflows.helpers.documents_helpers import string_array_to_documents


def retriever_node(state: RAGState):
    print("---RETRIEVER NODE---")
    chroma_service = ChromaService()

    question: str = state["messages"][-1].content

    documents: list[str] = chroma_service.query(question)[0]

    documents = string_array_to_documents(documents)

    return {"documents": documents}
