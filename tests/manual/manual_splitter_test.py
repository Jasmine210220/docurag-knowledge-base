from pathlib import Path

from docurag.processors import split_documents
from common import discover_test_sample_files, load_test_documents


PROJECT_ROOT = Path(__file__).resolve().parents[2]
TEST_SAMPLES_DIR = PROJECT_ROOT / "data" / "test_samples"


def main() -> None:
    if not TEST_SAMPLES_DIR.exists():
        print("Test samples directory does not exist.")
        return

    sample_files = discover_test_sample_files(TEST_SAMPLES_DIR)

    if not sample_files:
        print("No test sample files were found.")
        return

    loaded_documents, skipped_files = load_test_documents(sample_files)

    if not loaded_documents:
        print("No documents were available for splitting.")
        return

    chunks = split_documents(
        loaded_documents,
        chunk_size=80,
        chunk_overlap=20,
    )

    print(f"Loaded documents: {len(loaded_documents)}")
    print(f"Skipped files: {skipped_files}")
    print(f"Generated chunks: {len(chunks)}")

    for chunk in chunks[:5]:
        print("\n--- Chunk ---")
        print(f"Source: {chunk.metadata.get('source', 'unknown')}")
        print(f"Type: {chunk.metadata.get('file_type', 'unknown')}")
        print(f"Chunk index: {chunk.metadata.get('chunk_index', 'unknown')}")
        print(f"Preview: {chunk.page_content[:120]}")


if __name__ == "__main__":
    main()
