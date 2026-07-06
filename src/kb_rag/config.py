from dataclasses import dataclass
from pathlib import Path
import os

from dotenv import load_dotenv


# 先定位到项目根目录，后面很多路径都会基于它来拼接
BASE_DIR = Path(__file__).resolve().parents[2]

# data 目录用来存放项目运行过程中要用到的数据
DATA_DIR = BASE_DIR / "data"

# raw 目录放原始文档，比如 PDF、CSV、TXT、MD
RAW_DATA_DIR = DATA_DIR / "raw"

# vector_store 目录后续用来放向量索引等检索数据
VECTOR_STORE_DIR = DATA_DIR / "vector_store"


@dataclass
class Settings:
    # 大模型服务的 API Key，后续真正调用模型时会用到
    openai_api_key: str

    # 文本向量化时默认使用的 embedding 模型名称
    embedding_model: str

    # 问答阶段默认使用的聊天模型名称
    chat_model: str


def load_settings() -> Settings:
    # 先读取 .env 文件，把里面的配置加载到环境变量中
    load_dotenv()

    # 把项目需要的几个核心配置收口到一个 Settings 对象里统一返回
    return Settings(
        openai_api_key=os.getenv("OPENAI_API_KEY", ""),
        embedding_model=os.getenv("EMBEDDING_MODEL", "text-embedding-3-small"),
        chat_model=os.getenv("CHAT_MODEL", "gpt-4.1-mini"),
    )
