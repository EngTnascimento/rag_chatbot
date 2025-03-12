from langchain_core.documents import Document


def string_array_to_documents(documents: list[str]) -> list[Document]:
    return [Document(page_content=doc) for doc in documents]
