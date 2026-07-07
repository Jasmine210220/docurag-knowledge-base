from pathlib import Path

from langchain_core.documents import Document

from src.docurag.loaders.base import BaseDocumentLoader
from src.docurag.loaders.file_loaders import (
    CsvDocumentLoader,
    JsonDocumentLoader,
    PdfDocumentLoader,
    TextDocumentLoader,
)


# 用一个映射表统一管理“后缀名 -> 对应加载器”的关系
LOADER_MAPPING: dict[str, type[BaseDocumentLoader]] = {
    ".txt": TextDocumentLoader,
    ".md": TextDocumentLoader,
    ".json": JsonDocumentLoader,
    ".csv": CsvDocumentLoader,
    ".pdf": PdfDocumentLoader,
}


def get_loader(file_path: Path) -> BaseDocumentLoader:
    suffix = file_path.suffix.lower()
    loader_class = LOADER_MAPPING.get(suffix)

    if loader_class is None:
        raise ValueError(f"Unsupported file type: {suffix}")

    return loader_class(file_path)


def load_documents_from_directory(directory: Path) -> list[Document]:
    documents: list[Document] = []

    # 扫描目录下的所有文件，并按文件类型分发给对应加载器
    for file_path in sorted(directory.iterdir()):
        if not file_path.is_file():
            continue

        # 跳过 .gitkeep 这类目录占位文件，避免把非业务文件当成文档处理
        if file_path.name.startswith("."):
            continue

        # 当前还不支持的文件类型先直接跳过，避免整个流程因为单个文件中断
        if file_path.suffix.lower() not in LOADER_MAPPING:
            continue

        loader = get_loader(file_path)
        documents.extend(loader.load())

    return documents
