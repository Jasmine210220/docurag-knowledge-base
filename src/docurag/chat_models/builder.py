from langchain_community.chat_models import ChatTongyi
from langchain_core.language_models import BaseChatModel

from docurag.config import ChatModelSettings


def build_chat_model(settings: ChatModelSettings) -> BaseChatModel:
    if settings.provider != "dashscope":
        raise ValueError(f"Unsupported chat model provider: {settings.provider}")

    if not settings.api_key:
        raise ValueError("Chat model API key is not set.")

    return ChatTongyi(
        model=settings.model,
        api_key=settings.api_key,
    )
