import pytest

from docurag.chat_models import build_chat_model
from docurag.config import ChatModelSettings, EmbeddingModelSettings
from docurag.vectorstores import build_embeddings


def test_build_chat_model_rejects_unsupported_provider() -> None:
    settings = ChatModelSettings(
        provider="unsupported",
        model="test-model",
        api_key="test-key",
    )

    with pytest.raises(ValueError, match="Unsupported chat model provider"):
        build_chat_model(settings)


def test_build_chat_model_requires_api_key() -> None:
    settings = ChatModelSettings(
        provider="dashscope",
        model="qwen-max",
        api_key="",
    )

    with pytest.raises(ValueError, match="Chat model API key is not set"):
        build_chat_model(settings)


def test_build_embeddings_rejects_unsupported_provider() -> None:
    settings = EmbeddingModelSettings(
        provider="unsupported",
        model="embedding-model",
        api_key="test-key",
    )

    with pytest.raises(ValueError, match="Unsupported embedding provider"):
        build_embeddings(settings)


def test_build_embeddings_requires_api_key() -> None:
    settings = EmbeddingModelSettings(
        provider="dashscope",
        model="text-embedding-v1",
        api_key="",
    )

    with pytest.raises(ValueError, match="Embedding API key is not set"):
        build_embeddings(settings)
