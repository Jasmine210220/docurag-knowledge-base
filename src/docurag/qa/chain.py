from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains.retrieval import create_retrieval_chain
from langchain_core.language_models import BaseChatModel
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import Runnable


QA_SYSTEM_PROMPT = (
    "You are a helpful assistant for the DocuRAG project. "
    "Answer the user's question only with the provided context. "
    "If the context is insufficient, say you do not know.\n\n"
    "Context:\n{context}"
)


def build_qa_chain(
    retriever: Runnable,
    chat_model: BaseChatModel,
) -> Runnable:
    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", QA_SYSTEM_PROMPT),
            ("human", "{input}"),
        ]
    )
    document_chain = create_stuff_documents_chain(chat_model, prompt)
    return create_retrieval_chain(retriever, document_chain)
