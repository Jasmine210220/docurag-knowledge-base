from langchain_core.documents import Document
from langchain_core.language_models.fake_chat_models import FakeListChatModel
from langchain_core.runnables import RunnableLambda

from docurag.qa import build_qa_chain
from docurag.qa.chain import QA_SYSTEM_PROMPT


def test_qa_system_prompt_mentions_context_boundary() -> None:
    assert "provided context" in QA_SYSTEM_PROMPT
    assert "If the context is insufficient" in QA_SYSTEM_PROMPT


def test_build_qa_chain_returns_answer_and_context() -> None:
    documents = [
        Document(
            page_content="DocuRAG is a local RAG project.",
            metadata={"source": "a.txt", "chunk_index": 1},
        )
    ]

    fake_retriever = RunnableLambda(lambda _: documents)
    fake_chat_model = FakeListChatModel(
        responses=["DocuRAG is a local RAG project."]
    )

    qa_chain = build_qa_chain(
        retriever=fake_retriever,
        chat_model=fake_chat_model,
    )
    result = qa_chain.invoke({"input": "What is DocuRAG?"})

    assert result["answer"] == "DocuRAG is a local RAG project."
    assert len(result["context"]) == 1
    assert result["context"][0].metadata["source"] == "a.txt"
