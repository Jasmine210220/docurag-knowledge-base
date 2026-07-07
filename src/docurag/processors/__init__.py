"""文档处理模块。"""

from src.docurag.processors.text_splitter import (
    build_text_splitter,
    split_documents,
)

__all__ = [
    "build_text_splitter",
    "split_documents",
]
