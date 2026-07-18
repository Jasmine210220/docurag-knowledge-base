import argparse
from collections.abc import Sequence

from langchain_core.runnables import Runnable

from docurag.chat_models import build_chat_model
from docurag.config import Settings, load_settings
from docurag.qa import build_qa_chain
from docurag.vectorstores import ChromaVectorStoreManager, build_embeddings


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="python -m docurag.cli",
        description="DocuRAG command line interface",
    )
    mode_group = parser.add_mutually_exclusive_group(required=True)
    mode_group.add_argument(
        "--question",
        help="Ask one question with the current vector store.",
    )
    mode_group.add_argument(
        "--interactive",
        action="store_true",
        help="Start a simple interactive question loop.",
    )
    parser.add_argument(
        "--top-k",
        type=int,
        default=4,
        help="Number of retrieved context chunks. Default: 4.",
    )
    return parser


def build_cli_chain(settings: Settings, top_k: int) -> Runnable:
    embeddings = build_embeddings(settings.embedding)
    vector_store_manager = ChromaVectorStoreManager(
        settings=settings.vector_store,
        embeddings=embeddings,
    )
    vector_store = vector_store_manager.get_vector_store()
    snapshot = vector_store.get(limit=1, include=[])
    if not snapshot.get("ids"):
        raise ValueError(
            "Current vector store collection does not contain documents yet. "
            "Please index documents first."
        )

    retriever = vector_store.as_retriever(search_kwargs={"k": top_k})
    chat_model = build_chat_model(settings.chat)
    return build_qa_chain(retriever=retriever, chat_model=chat_model)


def print_qa_result(question: str, result: dict) -> None:
    print(f"Question: {question}")
    print(f"Answer: {result.get('answer', '')}")

    context = result.get("context", [])
    print(f"Context documents: {len(context)}")
    for index, document in enumerate(context, start=1):
        print(f"\n--- Context {index} ---")
        print(f"Source: {document.metadata.get('source', 'unknown')}")
        print(f"Chunk index: {document.metadata.get('chunk_index', 'unknown')}")
        print(f"Preview: {document.page_content[:120]}")


def ask_question(chain: Runnable, question: str) -> dict:
    return chain.invoke({"input": question})


def print_cli_error(message: str) -> None:
    print(f"Error: {message}")


def run_interactive_loop(chain: Runnable) -> int:
    print("DocuRAG CLI is ready. Type your question and press Enter.")
    print("Type exit or quit to stop.")

    while True:
        try:
            question = input("\nQuestion> ").strip()
        except KeyboardInterrupt:
            print("\nCLI session interrupted.")
            return 0
        except EOFError:
            print("\nCLI session ended.")
            return 0

        if not question:
            print("Please enter a non-empty question.")
            continue

        if question.lower() in {"exit", "quit"}:
            print("CLI session ended.")
            return 0

        try:
            result = ask_question(chain, question)
        except Exception as error:
            print_cli_error(f"Failed to answer question: {error}")
            continue

        print_qa_result(question, result)


def main(argv: Sequence[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(list(argv) if argv is not None else None)

    if args.top_k <= 0:
        parser.error("--top-k must be a positive integer.")

    settings = load_settings()

    try:
        chain = build_cli_chain(settings=settings, top_k=args.top_k)
    except ValueError as error:
        print_cli_error(str(error))
        return 1

    if args.question:
        try:
            result = ask_question(chain, args.question)
        except Exception as error:
            print_cli_error(f"Failed to answer question: {error}")
            return 1

        print_qa_result(args.question, result)
        return 0

    return run_interactive_loop(chain)


if __name__ == "__main__":
    raise SystemExit(main())
