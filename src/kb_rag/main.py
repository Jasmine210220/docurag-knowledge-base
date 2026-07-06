from pathlib import Path

from src.kb_rag.config import RAW_DATA_DIR, VECTOR_STORE_DIR, load_settings


def ensure_directories(paths: list[Path]) -> None:
    # 逐个检查目录是否存在，不存在就自动创建
    for path in paths:
        # parents=True 表示上层目录不存在时也一起创建
        # exist_ok=True 表示目录已经存在时不要报错
        path.mkdir(parents=True, exist_ok=True)


def main() -> None:
    # 程序启动时先把配置读进来
    settings = load_settings()

    # 再确保项目运行所需的基础目录已经准备好
    ensure_directories([RAW_DATA_DIR, VECTOR_STORE_DIR])

    # 下面这些输出先用于验证脚手架是否正常工作
    print("Project scaffold is ready.")
    print(f"Raw data directory: {RAW_DATA_DIR}")
    print(f"Vector store directory: {VECTOR_STORE_DIR}")
    print(f"Embedding model: {settings.embedding_model}")
    print(f"Chat model: {settings.chat_model}")

    # 如果还没配置 API Key，先给出提醒，避免后面调模型时才发现问题
    if not settings.openai_api_key:
        print("Warning: OPENAI_API_KEY is not set yet.")


if __name__ == "__main__":
    # 只有直接运行这个文件时，才会真正启动主程序
    main()
