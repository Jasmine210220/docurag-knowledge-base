from pathlib import Path
import shutil

from langchain_core.documents import Document

from docurag.loaders import get_loader
from docurag.vectorstores import ChromaVectorStoreManager


TEST_COLLECTION_NAME = "docurag_manual_test"


def has_test_store_artifacts(directory: Path) -> bool:
    if not directory.exists():
        return False

    return any(path.name != ".gitkeep" for path in directory.iterdir())


def collection_has_documents(vector_store_manager: ChromaVectorStoreManager) -> bool:
    snapshot = vector_store_manager.get_vector_store().get(limit=1, include=[])
    ids = snapshot.get("ids", [])
    return bool(ids)


def reset_test_vector_store(directory: Path) -> None:
    directory.mkdir(parents=True, exist_ok=True)

    for path in directory.iterdir():
        if path.name == ".gitkeep":
            continue

        if path.is_dir():
            shutil.rmtree(path)
        else:
            path.unlink()


def discover_test_sample_files(directory: Path) -> list[Path]:
    if not directory.exists():
        return []

    return [
        file_path
        for file_path in sorted(directory.iterdir())
        if file_path.is_file() and not file_path.name.startswith(".")
    ]


def load_test_documents(sample_files: list[Path]) -> tuple[list[Document], int]:
    documents: list[Document] = []
    skipped_files = 0

    for file_path in sample_files:
        try:
            loader = get_loader(file_path)
            documents.extend(loader.load())
        except Exception as error:
            skipped_files += 1
            print(f"Skipped file {file_path.name}: {error}")

    return documents, skipped_files
