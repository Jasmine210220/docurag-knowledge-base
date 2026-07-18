from pathlib import Path

from docurag.chat_models import build_chat_model
from docurag.config import TEST_VECTOR_STORE_DIR, load_settings
from docurag.qa import build_qa_chain
from docurag.retrievers import ChromaRetriever
from docurag.vectorstores import build_embeddings
from common import TEST_COLLECTION_NAME, collection_has_documents, has_test_store_artifacts


PROJECT_ROOT = Path(__file__).resolve().parents[2]


def main() -> None:
    settings = load_settings()

    if not TEST_VECTOR_STORE_DIR.exists():
        print(
            "Test vector store directory does not exist. "
            "Run manual_vector_index_test.py first."
        )
        return

    if not has_test_store_artifacts(TEST_VECTOR_STORE_DIR):
        print(
            "No non-placeholder test store artifacts were found in data/test_vector_store. "
            "Run manual_vector_index_test.py first."
        )
        return

    embeddings = build_embeddings(settings.embedding)
    retriever_builder = ChromaRetriever(
        settings=settings.vector_store.__class__(
            provider=settings.vector_store.provider,
            collection_name=TEST_COLLECTION_NAME,
            persist_directory=TEST_VECTOR_STORE_DIR,
        ),
        embeddings=embeddings,
    )

    if not collection_has_documents(retriever_builder.vector_store_manager):
        print(
            "The test collection does not currently expose any stored documents. "
            "Run manual_vector_index_test.py first."
        )
        return

    retriever = retriever_builder.vector_store_manager.get_vector_store().as_retriever(
        search_kwargs={"k": 2}
    )
    chat_model = build_chat_model(settings.chat)
    qa_chain = build_qa_chain(retriever=retriever, chat_model=chat_model)

    result = qa_chain.invoke({"input": "What is DocuRAG?"})

    print("Question: What is DocuRAG?")
    print(f"Answer: {result.get('answer', '')}")

    context = result.get("context", [])
    print(f"Context documents: {len(context)}")
    for index, document in enumerate(context, start=1):
        print(f"\n--- Context {index} ---")
        print(f"Source: {document.metadata.get('source', 'unknown')}")
        print(f"Chunk index: {document.metadata.get('chunk_index', 'unknown')}")
        print(f"Preview: {document.page_content[:120]}")


if __name__ == "__main__":
    main()
