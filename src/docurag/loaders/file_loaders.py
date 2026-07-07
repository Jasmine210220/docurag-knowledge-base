from langchain_core.documents import Document
from langchain_community.document_loaders import (
    CSVLoader,
    JSONLoader,
    PyPDFLoader,
    TextLoader,
)

from src.docurag.loaders.base import BaseDocumentLoader


class TextDocumentLoader(BaseDocumentLoader):
    # TXT 和 MD 当前都直接交给 LangChain 的 TextLoader 处理
    def load(self) -> list[Document]:
        loader = TextLoader(str(self.file_path), encoding="utf-8")
        documents = loader.load()
        return self.merge_metadata(documents)


class JsonDocumentLoader(BaseDocumentLoader):
    def load(self) -> list[Document]:
        # JSONLoader 依赖 jq 语法：
        # . 表示把整个 JSON 对象当成一个文档
        # 这样当前阶段先保证结构简单、容易理解
        try:
            loader = JSONLoader(
                file_path=str(self.file_path),
                jq_schema=".",
                text_content=False,
            )
            documents = loader.load()
        except ImportError as error:
            # JSONLoader 需要额外安装 jq，先把报错包装成更容易理解的提示
            raise RuntimeError(
                "JSON loading requires the 'jq' package. Install it before loading .json files."
            ) from error

        return self.merge_metadata(documents)


class CsvDocumentLoader(BaseDocumentLoader):
    def load(self) -> list[Document]:
        # CSVLoader 会把每一行记录加载成一个 Document
        loader = CSVLoader(str(self.file_path), encoding="utf-8")
        documents = loader.load()
        return self.merge_metadata(documents)


class PdfDocumentLoader(BaseDocumentLoader):
    def load(self) -> list[Document]:
        # PDF 直接交给 LangChain 的 PyPDFLoader，它默认按页返回 Document
        loader = PyPDFLoader(str(self.file_path))
        documents = loader.load()
        return self.merge_metadata(documents)
