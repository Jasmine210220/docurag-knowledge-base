from dataclasses import dataclass
import os
from pathlib import Path

from dotenv import load_dotenv


BASE_DIR = Path(__file__).resolve().parents[2]
DATA_DIR = BASE_DIR / "data"
RAW_DATA_DIR = DATA_DIR / "raw"
VECTOR_STORE_DIR = DATA_DIR / "vector_store"
TEST_VECTOR_STORE_DIR = DATA_DIR / "test_vector_store"


@dataclass
class ChatModelSettings:
    provider: str
    model: str
    api_key: str


@dataclass
class EmbeddingModelSettings:
    provider: str
    model: str
    api_key: str


@dataclass
class VectorStoreSettings:
    provider: str
    collection_name: str
    persist_directory: Path


@dataclass
class Settings:
    chat: ChatModelSettings
    embedding: EmbeddingModelSettings
    vector_store: VectorStoreSettings


def load_settings() -> Settings:
    load_dotenv()

    return Settings(
        chat=ChatModelSettings(
            provider=os.getenv("CHAT_MODEL_PROVIDER", "dashscope"),
            model=os.getenv("CHAT_MODEL", "qwen-max"),
            api_key=os.getenv("CHAT_API_KEY", os.getenv("DASHSCOPE_API_KEY", "")),
        ),
        embedding=EmbeddingModelSettings(
            provider=os.getenv("EMBEDDING_PROVIDER", "dashscope"),
            model=os.getenv("EMBEDDING_MODEL", "text-embedding-v1"),
            api_key=os.getenv("EMBEDDING_API_KEY", os.getenv("DASHSCOPE_API_KEY", "")),
        ),
        vector_store=VectorStoreSettings(
            provider=os.getenv("VECTOR_STORE_PROVIDER", "chroma"),
            collection_name=os.getenv("VECTOR_COLLECTION_NAME", "docurag_documents"),
            persist_directory=Path(os.getenv("VECTOR_STORE_DIR", str(VECTOR_STORE_DIR))),
        ),
    )
