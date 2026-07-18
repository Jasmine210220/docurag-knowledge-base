from langchain_core.documents import Document
from langchain_core.embeddings import Embeddings

from docurag.config import VectorStoreSettings
from docurag.vectorstores.chroma_store import ChromaVectorStoreManager


class ChromaRetriever:
    def __init__(
        self,
        settings: VectorStoreSettings,
        embeddings: Embeddings,
    ) -> None:
        self.vector_store_manager = ChromaVectorStoreManager(
            settings=settings,
            embeddings=embeddings,
        )

    def retrieve(self, query: str, k: int = 4) -> list[Document]:
        vector_store = self.vector_store_manager.get_vector_store()
        return vector_store.similarity_search(query, k=k)
