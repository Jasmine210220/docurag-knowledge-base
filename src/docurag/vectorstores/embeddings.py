from langchain_community.embeddings import DashScopeEmbeddings
from langchain_core.embeddings import Embeddings

from docurag.config import EmbeddingModelSettings


def build_embeddings(settings: EmbeddingModelSettings) -> Embeddings:
    if settings.provider != "dashscope":
        raise ValueError(f"Unsupported embedding provider: {settings.provider}")

    if not settings.api_key:
        raise ValueError("Embedding API key is not set.")

    return DashScopeEmbeddings(
        model=settings.model,
        dashscope_api_key=settings.api_key,
    )
