from pathlib import Path

from docurag.config import RAW_DATA_DIR, load_settings
from docurag.loaders import load_documents_from_directory


def ensure_directories(paths: list[Path]) -> None:
    for path in paths:
        path.mkdir(parents=True, exist_ok=True)


def main() -> None:
    settings = load_settings()
    ensure_directories([RAW_DATA_DIR, settings.vector_store.persist_directory])

    print("Project scaffold is ready.")
    print(f"Raw data directory: {RAW_DATA_DIR}")
    print(f"Vector store directory: {settings.vector_store.persist_directory}")
    print(f"Chat model provider: {settings.chat.provider}")
    print(f"Chat model: {settings.chat.model}")
    print(f"Embedding provider: {settings.embedding.provider}")
    print(f"Embedding model: {settings.embedding.model}")

    if not settings.chat.api_key:
        print("Warning: chat model API key is not set yet.")

    if not settings.embedding.api_key:
        print("Warning: embedding model API key is not set yet.")

    load_result = load_documents_from_directory(RAW_DATA_DIR)

    for file_name, error in load_result.failed_files:
        print(f"Skipped file {file_name}: {error}")

    documents = load_result.documents
    print(f"Loaded documents: {len(documents)}")

    if documents:
        first_document = documents[0]
        print(f"First document source: {first_document.metadata['source']}")
        print(f"First document type: {first_document.metadata['file_type']}")
        print(f"First document preview: {first_document.page_content[:100]}")
    else:
        print("No documents found in raw data directory yet.")


if __name__ == "__main__":
    main()
