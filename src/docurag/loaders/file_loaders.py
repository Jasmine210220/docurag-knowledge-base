from langchain_community.document_loaders import (
    CSVLoader,
    JSONLoader,
    PyPDFLoader,
    TextLoader,
)
from langchain_core.documents import Document

from docurag.loaders.base import BaseDocumentLoader


class TextDocumentLoader(BaseDocumentLoader):
    def load(self) -> list[Document]:
        loader = TextLoader(str(self.file_path), encoding="utf-8")
        documents = loader.load()
        return self.merge_metadata(documents)


class JsonDocumentLoader(BaseDocumentLoader):
    def load(self) -> list[Document]:
        try:
            loader = JSONLoader(
                file_path=str(self.file_path),
                jq_schema=".",
                text_content=False,
            )
            documents = loader.load()
        except ImportError as error:
            raise RuntimeError(
                "JSON loading requires the 'jq' package. Install it before loading .json files."
            ) from error

        return self.merge_metadata(documents)


class CsvDocumentLoader(BaseDocumentLoader):
    def load(self) -> list[Document]:
        loader = CSVLoader(str(self.file_path), encoding="utf-8")
        documents = loader.load()
        return self.merge_metadata(documents)


class PdfDocumentLoader(BaseDocumentLoader):
    def load(self) -> list[Document]:
        loader = PyPDFLoader(str(self.file_path))
        documents = loader.load()
        return self.merge_metadata(documents)
