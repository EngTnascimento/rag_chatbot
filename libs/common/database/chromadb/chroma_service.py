from .chroma_config import ChromaConfig
from libs.common.llm_providers.openai.services.openai_service import OpenaiService
import chromadb
import uuid
from langchain_core.documents import Document


class ChromaService:
    def __init__(
        self,
        llm_service: OpenaiService = OpenaiService(),
    ):
        config = ChromaConfig(embedding_function=llm_service.embeddings)
        self.client = chromadb.HttpClient(
            host="chromadb",
            port=8000,
            headers={"Content-Type": "application/json"},
        )
        self.client.heartbeat()
        self.collection = self.client.get_or_create_collection(
            name=config.collection_name,
            embedding_function=config.embedding_function,
        )

    @staticmethod
    def documents_to_string_array(documents: list[Document]):
        return [doc.page_content for doc in documents]

    def add_documents(self, documents: list[str]):
        # Ensure documents are non-empty and properly formatted
        valid_documents = [doc for doc in documents if doc and isinstance(doc, str)]
        if not valid_documents:
            print("Warning: No valid documents to add")
            return

        try:
            # Process documents in chunks of 100
            chunk_size = 200
            for i in range(0, len(valid_documents), chunk_size):
                chunk = valid_documents[i : i + chunk_size]
                self.collection.add(
                    documents=chunk,
                    ids=[str(uuid.uuid4()) for _ in chunk],
                )
                print(f"Added chunk {i // chunk_size + 1} ({len(chunk)} documents)")

            print(f"Successfully added all {len(valid_documents)} documents")
        except Exception as e:
            print(f"Error adding documents: {str(e)}")
            raise

    def query(self, query: str, k: int = 10) -> list[str]:
        documents = self.collection.query(query_texts=[query], n_results=k)
        return documents["documents"]
