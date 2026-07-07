"""文档加载模块。"""

from langchain_core.documents import Document

from src.docurag.loaders.base import BaseDocumentLoader
from src.docurag.loaders.factory import get_loader, load_documents_from_directory

__all__ = [
    "BaseDocumentLoader",
    "Document",
    "get_loader",
    "load_documents_from_directory",
]
