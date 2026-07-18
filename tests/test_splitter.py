from langchain_core.documents import Document

from docurag.processors import split_documents


def test_split_documents_preserves_metadata_and_adds_chunk_index() -> None:
    documents = [
        Document(
            page_content="A" * 120,
            metadata={"source": "unit-test.txt", "file_type": ".txt", "custom": "value"},
        )
    ]

    chunks = split_documents(documents, chunk_size=50, chunk_overlap=10)

    assert len(chunks) > 1
    assert [chunk.metadata["chunk_index"] for chunk in chunks] == list(
        range(1, len(chunks) + 1)
    )
    assert all(chunk.metadata["source"] == "unit-test.txt" for chunk in chunks)
    assert all(chunk.metadata["file_type"] == ".txt" for chunk in chunks)
    assert all(chunk.metadata["custom"] == "value" for chunk in chunks)
