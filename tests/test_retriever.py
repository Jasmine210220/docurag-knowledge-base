from pathlib import Path

from langchain_core.documents import Document

from docurag.config import VectorStoreSettings
from docurag.retrievers import ChromaRetriever


class FakeEmbeddings:
    def embed_documents(self, texts: list[str]) -> list[list[float]]:
        return [self._embed_text(text) for text in texts]

    def embed_query(self, text: str) -> list[float]:
        return self._embed_text(text)

    @staticmethod
    def _embed_text(text: str) -> list[float]:
        lowered = text.lower()
        tokens = set(lowered.split())
        overlap_score = float(len(tokens & {"docurag", "project"}))
        has_docurag = 1.0 if "docurag" in tokens else 0.0
        has_project = 1.0 if "project" in tokens else 0.0
        return [overlap_score, has_docurag, has_project]


def test_chroma_retriever_returns_most_relevant_document(tmp_path: Path) -> None:
    settings = VectorStoreSettings(
        provider="chroma",
        collection_name="unit_test_retriever",
        persist_directory=tmp_path,
    )
    retriever = ChromaRetriever(settings=settings, embeddings=FakeEmbeddings())

    vector_store = retriever.vector_store_manager.index_documents(
        [
            Document(
                page_content="DocuRAG project introduction and overview",
                metadata={"source": "a.txt", "chunk_index": 1},
            ),
            Document(
                page_content="Another unrelated sample about gardening",
                metadata={"source": "b.txt", "chunk_index": 2},
            ),
        ]
    )

    results = retriever.retrieve("DocuRAG project", k=1)

    assert len(results) == 1
    assert results[0].metadata["source"] == "a.txt"
    assert vector_store is not None
