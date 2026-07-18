from pathlib import Path

import pytest
from langchain_core.documents import Document

from docurag.cli import ask_question, main, run_interactive_loop
from docurag.config import (
    ChatModelSettings,
    EmbeddingModelSettings,
    Settings,
    VectorStoreSettings,
)


class FakeVectorStore:
    def __init__(self, documents: list[Document]) -> None:
        self.documents = documents

    def get(self, limit: int = 1, include: list[str] | None = None) -> dict:
        if self.documents[:limit]:
            return {"ids": ["doc-1"]}
        return {"ids": []}

    def as_retriever(self, search_kwargs: dict | None = None) -> object:
        return {"documents": self.documents, "search_kwargs": search_kwargs or {}}


class FakeVectorStoreManager:
    documents: list[Document] = []

    def __init__(self, settings: VectorStoreSettings, embeddings: object) -> None:
        self.settings = settings
        self.embeddings = embeddings

    def get_vector_store(self) -> FakeVectorStore:
        return FakeVectorStore(self.documents)


def build_test_settings(tmp_path: Path) -> Settings:
    return Settings(
        chat=ChatModelSettings(
            provider="dashscope",
            model="qwen-max",
            api_key="chat-key",
        ),
        embedding=EmbeddingModelSettings(
            provider="dashscope",
            model="text-embedding-v1",
            api_key="embedding-key",
        ),
        vector_store=VectorStoreSettings(
            provider="chroma",
            collection_name="test_cli",
            persist_directory=tmp_path,
        ),
    )


def test_ask_question_invokes_chain_input() -> None:
    class FakeChain:
        def invoke(self, payload: dict) -> dict:
            assert payload == {"input": "What is DocuRAG?"}
            return {"answer": "A local RAG project.", "context": []}

    result = ask_question(FakeChain(), "What is DocuRAG?")

    assert result["answer"] == "A local RAG project."


def test_cli_question_mode_prints_answer_and_context(
    monkeypatch, capsys, tmp_path: Path
) -> None:
    settings = build_test_settings(tmp_path)
    FakeVectorStoreManager.documents = [
        Document(
            page_content="DocuRAG is a local document QA project.",
            metadata={"source": "a.txt", "chunk_index": 1},
        )
    ]

    monkeypatch.setattr("docurag.cli.load_settings", lambda: settings)
    monkeypatch.setattr("docurag.cli.build_embeddings", lambda _: object())
    monkeypatch.setattr("docurag.cli.build_chat_model", lambda _: object())
    monkeypatch.setattr("docurag.cli.ChromaVectorStoreManager", FakeVectorStoreManager)

    def fake_build_qa_chain(retriever: object, chat_model: object) -> object:
        class FakeChain:
            def invoke(self, payload: dict) -> dict:
                assert payload["input"] == "What is DocuRAG?"
                assert retriever["search_kwargs"] == {"k": 2}
                assert chat_model is not None
                return {
                    "answer": "DocuRAG is a local document QA project.",
                    "context": retriever["documents"],
                }

        return FakeChain()

    monkeypatch.setattr("docurag.cli.build_qa_chain", fake_build_qa_chain)

    exit_code = main(["--question", "What is DocuRAG?", "--top-k", "2"])

    captured = capsys.readouterr()
    assert exit_code == 0
    assert "Question: What is DocuRAG?" in captured.out
    assert "Answer: DocuRAG is a local document QA project." in captured.out
    assert "Source: a.txt" in captured.out


def test_cli_requires_indexed_documents(monkeypatch, capsys, tmp_path: Path) -> None:
    settings = build_test_settings(tmp_path)
    FakeVectorStoreManager.documents = []

    monkeypatch.setattr("docurag.cli.load_settings", lambda: settings)
    monkeypatch.setattr("docurag.cli.build_embeddings", lambda _: object())
    monkeypatch.setattr("docurag.cli.ChromaVectorStoreManager", FakeVectorStoreManager)

    exit_code = main(["--question", "What is DocuRAG?"])

    captured = capsys.readouterr()
    assert exit_code == 1
    assert "does not contain documents yet" in captured.out


def test_cli_question_mode_returns_non_zero_when_qa_call_fails(
    monkeypatch, capsys, tmp_path: Path
) -> None:
    settings = build_test_settings(tmp_path)
    FakeVectorStoreManager.documents = [
        Document(
            page_content="DocuRAG is a local document QA project.",
            metadata={"source": "a.txt", "chunk_index": 1},
        )
    ]

    monkeypatch.setattr("docurag.cli.load_settings", lambda: settings)
    monkeypatch.setattr("docurag.cli.build_embeddings", lambda _: object())
    monkeypatch.setattr("docurag.cli.build_chat_model", lambda _: object())
    monkeypatch.setattr("docurag.cli.ChromaVectorStoreManager", FakeVectorStoreManager)

    def fake_build_qa_chain(retriever: object, chat_model: object) -> object:
        class FailingChain:
            def invoke(self, payload: dict) -> dict:
                raise RuntimeError("simulated qa failure")

        return FailingChain()

    monkeypatch.setattr("docurag.cli.build_qa_chain", fake_build_qa_chain)

    exit_code = main(["--question", "What is DocuRAG?"])

    captured = capsys.readouterr()
    assert exit_code == 1
    assert "Error: Failed to answer question: simulated qa failure" in captured.out


@pytest.mark.parametrize(
    ("input_side_effect", "expected_message"),
    [
        ("quit", "CLI session ended."),
        (KeyboardInterrupt, "CLI session interrupted."),
        (EOFError, "CLI session ended."),
    ],
)
def test_interactive_loop_exits_cleanly_on_common_exit_paths(
    monkeypatch, capsys, input_side_effect: str | type[BaseException], expected_message: str
) -> None:
    class FakeChain:
        def invoke(self, payload: dict) -> dict:
            raise AssertionError("invoke should not be called on direct exit paths")

    def fake_input(prompt: str) -> str:
        if isinstance(input_side_effect, str):
            return input_side_effect
        raise input_side_effect

    monkeypatch.setattr("builtins.input", fake_input)

    exit_code = run_interactive_loop(FakeChain())

    captured = capsys.readouterr()
    assert exit_code == 0
    assert expected_message in captured.out


def test_interactive_loop_continues_after_qa_failure(monkeypatch, capsys) -> None:
    class FailingChain:
        def __init__(self) -> None:
            self.calls = 0

        def invoke(self, payload: dict) -> dict:
            self.calls += 1
            raise RuntimeError("temporary failure")

    answers = iter(["What is DocuRAG?", "exit"])
    monkeypatch.setattr("builtins.input", lambda _: next(answers))

    chain = FailingChain()
    exit_code = run_interactive_loop(chain)

    captured = capsys.readouterr()
    assert exit_code == 0
    assert chain.calls == 1
    assert "Error: Failed to answer question: temporary failure" in captured.out
    assert "CLI session ended." in captured.out
