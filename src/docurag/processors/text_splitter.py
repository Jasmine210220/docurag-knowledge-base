from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter


def build_text_splitter(
    chunk_size: int = 500,
    chunk_overlap: int = 100,
) -> RecursiveCharacterTextSplitter:
    # 这里直接使用 LangChain 官方常见的 RecursiveCharacterTextSplitter。
    # 它会优先按照更自然的边界去切文本，切不动时再逐步退化到更小的分隔方式。
    return RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        separators=["\n\n", "\n", " ", ""],
    )


def split_documents(
    documents: list[Document],
    chunk_size: int = 500,
    chunk_overlap: int = 100,
) -> list[Document]:
    # 这个函数的职责很单纯：
    # 接收已经加载好的 Document 列表，再交给 LangChain 切分器产出 chunk 级别的 Document 列表。
    splitter = build_text_splitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
    )
    chunks = splitter.split_documents(documents)

    # LangChain 在切分时会保留原始 metadata。
    # 这里再补一个 chunk_index，方便后面调试、打印和结果溯源。
    normalized_chunks: list[Document] = []
    for index, chunk in enumerate(chunks, start=1):
        chunk.metadata["chunk_index"] = index
        normalized_chunks.append(chunk)

    return normalized_chunks
