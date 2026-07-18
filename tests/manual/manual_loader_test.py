from pathlib import Path

from docurag.loaders import get_loader


PROJECT_ROOT = Path(__file__).resolve().parents[2]
TEST_SAMPLES_DIR = PROJECT_ROOT / "data" / "test_samples"


def main() -> None:
    if not TEST_SAMPLES_DIR.exists():
        print("Test samples directory does not exist.")
        return

    sample_files = [
        file_path
        for file_path in sorted(TEST_SAMPLES_DIR.iterdir())
        if file_path.is_file() and not file_path.name.startswith(".")
    ]

    if not sample_files:
        print("No test sample files were found.")
        return

    total_documents = 0
    success_count = 0
    failure_count = 0

    print(f"Discovered test sample files: {len(sample_files)}")

    for file_path in sample_files:
        print(f"\n=== Testing file: {file_path.name} ===")

        try:
            loader = get_loader(file_path)
            print(f"Using loader: {loader.__class__.__name__}")

            documents = loader.load()
            print(f"Returned documents: {len(documents)}")

            total_documents += len(documents)
            success_count += 1

            for index, document in enumerate(documents, start=1):
                print(f"\n--- Document {index} ---")
                print(f"Source: {document.metadata.get('source', 'unknown')}")
                print(f"Type: {document.metadata.get('file_type', 'unknown')}")
                print(f"Preview: {document.page_content[:100]}")
        except Exception as error:
            failure_count += 1
            print(f"Loading failed: {error}")

    print("\n=== Summary ===")
    print(f"Successful files: {success_count}")
    print(f"Failed files: {failure_count}")
    print(f"Total documents: {total_documents}")


if __name__ == "__main__":
    main()
