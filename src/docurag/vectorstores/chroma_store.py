from pathlib import Path

from langchain_chroma import Chroma
from langchain_core.documents import Document
from langchain_core.embeddings import Embeddings

from docurag.config import VectorStoreSettings


class ChromaVectorStoreManager:
    def __init__(
        self,
        settings: VectorStoreSettings,
        embeddings: Embeddings,
    ) -> None:
        if settings.provider != "chroma":
            raise ValueError(f"Unsupported vector store provider: {settings.provider}")

        self.settings = settings
        self.embeddings = embeddings

    def _ensure_persist_directory(self) -> Path:
        self.settings.persist_directory.mkdir(parents=True, exist_ok=True)
        return self.settings.persist_directory

    def get_vector_store(self) -> Chroma:
        persist_directory = self._ensure_persist_directory()
        return Chroma(
            collection_name=self.settings.collection_name,
            persist_directory=str(persist_directory),
            embedding_function=self.embeddings,
        )

    def index_documents(self, documents: list[Document]) -> Chroma:
        vector_store = self.get_vector_store()

        if documents:
            vector_store.add_documents(documents)

        return vector_store
