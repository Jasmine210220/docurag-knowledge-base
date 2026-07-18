from pathlib import Path

from docurag.config import VECTOR_STORE_DIR, load_settings


def test_load_settings_uses_defaults(monkeypatch) -> None:
    monkeypatch.delenv("CHAT_MODEL_PROVIDER", raising=False)
    monkeypatch.delenv("CHAT_MODEL", raising=False)
    monkeypatch.delenv("CHAT_API_KEY", raising=False)
    monkeypatch.delenv("DASHSCOPE_API_KEY", raising=False)
    monkeypatch.delenv("EMBEDDING_PROVIDER", raising=False)
    monkeypatch.delenv("EMBEDDING_MODEL", raising=False)
    monkeypatch.delenv("EMBEDDING_API_KEY", raising=False)
    monkeypatch.delenv("VECTOR_STORE_PROVIDER", raising=False)
    monkeypatch.delenv("VECTOR_COLLECTION_NAME", raising=False)
    monkeypatch.delenv("VECTOR_STORE_DIR", raising=False)

    settings = load_settings()

    assert settings.chat.provider == "dashscope"
    assert settings.chat.model == "qwen-max"
    assert settings.chat.api_key == ""
    assert settings.embedding.provider == "dashscope"
    assert settings.embedding.model == "text-embedding-v1"
    assert settings.embedding.api_key == ""
    assert settings.vector_store.provider == "chroma"
    assert settings.vector_store.collection_name == "docurag_documents"
    assert settings.vector_store.persist_directory == VECTOR_STORE_DIR


def test_load_settings_honors_environment_overrides(monkeypatch, tmp_path: Path) -> None:
    monkeypatch.setenv("CHAT_MODEL_PROVIDER", "custom-chat")
    monkeypatch.setenv("CHAT_MODEL", "chat-model")
    monkeypatch.setenv("CHAT_API_KEY", "chat-key")
    monkeypatch.setenv("EMBEDDING_PROVIDER", "custom-embedding")
    monkeypatch.setenv("EMBEDDING_MODEL", "embedding-model")
    monkeypatch.setenv("EMBEDDING_API_KEY", "embedding-key")
    monkeypatch.setenv("VECTOR_STORE_PROVIDER", "custom-store")
    monkeypatch.setenv("VECTOR_COLLECTION_NAME", "custom-collection")
    monkeypatch.setenv("VECTOR_STORE_DIR", str(tmp_path))

    settings = load_settings()

    assert settings.chat.provider == "custom-chat"
    assert settings.chat.model == "chat-model"
    assert settings.chat.api_key == "chat-key"
    assert settings.embedding.provider == "custom-embedding"
    assert settings.embedding.model == "embedding-model"
    assert settings.embedding.api_key == "embedding-key"
    assert settings.vector_store.provider == "custom-store"
    assert settings.vector_store.collection_name == "custom-collection"
    assert settings.vector_store.persist_directory == tmp_path
