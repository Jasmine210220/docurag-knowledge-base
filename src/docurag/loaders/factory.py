from dataclasses import dataclass
from pathlib import Path

from langchain_core.documents import Document

from docurag.loaders.base import BaseDocumentLoader
from docurag.loaders.file_loaders import (
    CsvDocumentLoader,
    JsonDocumentLoader,
    PdfDocumentLoader,
    TextDocumentLoader,
)


LOADER_MAPPING: dict[str, type[BaseDocumentLoader]] = {
    ".txt": TextDocumentLoader,
    ".md": TextDocumentLoader,
    ".json": JsonDocumentLoader,
    ".csv": CsvDocumentLoader,
    ".pdf": PdfDocumentLoader,
}


@dataclass
class DirectoryLoadResult:
    documents: list[Document]
    failed_files: list[tuple[str, Exception]]


def get_loader(file_path: Path) -> BaseDocumentLoader:
    suffix = file_path.suffix.lower()
    loader_class = LOADER_MAPPING.get(suffix)

    if loader_class is None:
        raise ValueError(f"Unsupported file type: {suffix}")

    return loader_class(file_path)


def load_documents_from_directory(directory: Path) -> DirectoryLoadResult:
    documents: list[Document] = []
    failed_files: list[tuple[str, Exception]] = []

    for file_path in sorted(directory.iterdir()):
        if not file_path.is_file():
            continue

        if file_path.name.startswith("."):
            continue

        if file_path.suffix.lower() not in LOADER_MAPPING:
            continue

        try:
            loader = get_loader(file_path)
            documents.extend(loader.load())
        except Exception as error:
            failed_files.append((file_path.name, error))

    return DirectoryLoadResult(
        documents=documents,
        failed_files=failed_files,
    )
