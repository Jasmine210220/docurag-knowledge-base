from pathlib import Path

from docurag.config import TEST_VECTOR_STORE_DIR, load_settings
from docurag.retrievers import ChromaRetriever
from docurag.vectorstores import build_embeddings
from common import TEST_COLLECTION_NAME, collection_has_documents, has_test_store_artifacts


PROJECT_ROOT = Path(__file__).resolve().parents[2]


def main() -> None:
    settings = load_settings()

    if not TEST_VECTOR_STORE_DIR.exists():
        print(
            "Test vector store directory does not exist. "
            "Run manual_vector_index_test.py first."
        )
        return

    if not has_test_store_artifacts(TEST_VECTOR_STORE_DIR):
        print(
            "No non-placeholder test store artifacts were found in data/test_vector_store. "
            "Run manual_vector_index_test.py first."
        )
        return

    embeddings = build_embeddings(settings.embedding)
    retriever = ChromaRetriever(
        settings=settings.vector_store.__class__(
            provider=settings.vector_store.provider,
            collection_name=TEST_COLLECTION_NAME,
            persist_directory=TEST_VECTOR_STORE_DIR,
        ),
        embeddings=embeddings,
    )

    if not collection_has_documents(retriever.vector_store_manager):
        print(
            "The test collection does not currently expose any stored documents. "
            "Run manual_vector_index_test.py first."
        )
        return

    results = retriever.retrieve("DocuRAG project", k=2)

    print(f"Retriever results: {len(results)}")

    for index, result in enumerate(results, start=1):
        print(f"\n--- Result {index} ---")
        print(f"Source: {result.metadata.get('source', 'unknown')}")
        print(f"Chunk index: {result.metadata.get('chunk_index', 'unknown')}")
        print(f"Preview: {result.page_content[:120]}")


if __name__ == "__main__":
    main()
