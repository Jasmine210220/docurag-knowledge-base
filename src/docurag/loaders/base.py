from abc import ABC, abstractmethod
from pathlib import Path

from langchain_core.documents import Document


class BaseDocumentLoader(ABC):
    # 所有加载器都接收一个文件路径，后续子类只需要专注于自己的读取逻辑
    def __init__(self, file_path: Path) -> None:
        self.file_path = file_path

    @abstractmethod
    def load(self) -> list[Document]:
        # 统一规定：每个加载器最终都返回 LangChain 官方的 Document 列表
        raise NotImplementedError

    def build_metadata(self) -> dict[str, str]:
        # 先把各类文档都会用到的公共元数据统一整理好
        return {
            "source": str(self.file_path),
            "file_name": self.file_path.name,
            "file_type": self.file_path.suffix.lower(),
        }

    def merge_metadata(self, documents: list[Document]) -> list[Document]:
        # LangChain loader 自己也可能生成 metadata，这里把项目公共元数据补进去并保留原始信息
        base_metadata = self.build_metadata()
        normalized_documents: list[Document] = []

        for document in documents:
            merged_metadata = {**document.metadata, **base_metadata}
            normalized_documents.append(
                Document(
                    page_content=document.page_content,
                    metadata=merged_metadata,
                )
            )

        return normalized_documents
