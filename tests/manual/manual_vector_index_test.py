from pathlib import Path

from docurag.config import TEST_VECTOR_STORE_DIR, load_settings
from docurag.processors import split_documents
from docurag.vectorstores import ChromaVectorStoreManager, build_embeddings
from common import (
    TEST_COLLECTION_NAME,
    discover_test_sample_files,
    load_test_documents,
    reset_test_vector_store,
)


PROJECT_ROOT = Path(__file__).resolve().parents[2]
TEST_SAMPLES_DIR = PROJECT_ROOT / "data" / "test_samples"


def main() -> None:
    settings = load_settings()

    if not TEST_SAMPLES_DIR.exists():
        print("Test samples directory does not exist.")
        return

    sample_files = discover_test_sample_files(TEST_SAMPLES_DIR)

    documents, skipped_files = load_test_documents(sample_files)

    if not documents:
        print("No supported test documents were loaded.")
        return

    chunks = split_documents(documents, chunk_size=80, chunk_overlap=20)
    if not chunks:
        print("No chunks were produced.")
        return

    test_store_dir = TEST_VECTOR_STORE_DIR
    reset_test_vector_store(test_store_dir)

    embeddings = build_embeddings(settings.embedding)
    vector_store_manager = ChromaVectorStoreManager(
        settings=settings.vector_store.__class__(
            provider=settings.vector_store.provider,
            collection_name=TEST_COLLECTION_NAME,
            persist_directory=test_store_dir,
        ),
        embeddings=embeddings,
    )
    vector_store = vector_store_manager.index_documents(chunks)

    results = vector_store.similarity_search("DocuRAG project", k=2)

    print(f"Loaded documents: {len(documents)}")
    print(f"Skipped files: {skipped_files}")
    print(f"Generated chunks: {len(chunks)}")
    print(f"Test vector store directory: {test_store_dir}")
    print("Test vector store was reset before indexing.")
    print(f"Similarity search results: {len(results)}")

    for index, result in enumerate(results, start=1):
        print(f"\n--- Result {index} ---")
        print(f"Source: {result.metadata.get('source', 'unknown')}")
        print(f"Chunk index: {result.metadata.get('chunk_index', 'unknown')}")
        print(f"Preview: {result.page_content[:120]}")


if __name__ == "__main__":
    main()
