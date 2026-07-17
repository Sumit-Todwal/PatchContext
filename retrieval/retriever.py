from langchain_core.documents import Document

from vectorstore.faiss_store import get_vectorstore
from utils.logger import logger

from config import (
    SEARCH_TYPE,
    TOP_K,
    FETCH_K,
    LAMBDA_MULT,
    MAX_CONTEXT_CHARS,
)


def get_retriever():
    """
    Create and return the LangChain retriever.
    """

    logger.info("Loading FAISS vector store...")

    vectorstore = get_vectorstore()

    logger.info("Creating retriever...")

    retriever = vectorstore.as_retriever(
        search_type=SEARCH_TYPE,
        search_kwargs={
            "k": TOP_K,
            "fetch_k": FETCH_K,
            "lambda_mult": LAMBDA_MULT,
        },
    )

    logger.info("Retriever created successfully.")

    return retriever


# Create the retriever once and reuse it
retriever = get_retriever()


def retrieve_documents(question: str) -> list[Document]:
    """
    Retrieve relevant documents for a user question.
    """

    logger.info(f"Searching for question: {question}")

    documents = retriever.invoke(question)

    logger.info(f"Retrieved {len(documents)} documents.")

    return documents


def format_documents(documents: list[Document]) -> str:
    """
    Convert retrieved documents into structured context for the LLM.
    """

    unique_documents = []
    seen = set()

    # Remove duplicate chunks
    for document in documents:

        unique_id = (
            document.metadata.get("chunk_id")
            or document.metadata.get("id")
            or document.page_content
        )

        if unique_id in seen:
            continue

        seen.add(unique_id)
        unique_documents.append(document)

    formatted_documents = []

    separator = "\n\n" + "=" * 80 + "\n\n"

    priority_fields = [
        "type",
        "number",
        "pr_number",
        "issue_number",
        "title",
        "author",
        "state",
        "comment_type",
        "created_at",
        "merged_at",
        "closed_at",
        "sha",
        "url",
    ]

    for index, document in enumerate(unique_documents, start=1):

        metadata = document.metadata

        content = document.page_content.strip()

        if len(content) > MAX_CONTEXT_CHARS:
            content = (
                content[:MAX_CONTEXT_CHARS]
                + "\n...(truncated)"
            )

        lines = [
            f"Document {index}",
            ""
        ]

        displayed = set()

        # Display important metadata first
        for field in priority_fields:

            value = metadata.get(field)

            if value in (None, "", [], {}):
                continue

            pretty_key = field.replace("_", " ").title()

            lines.append(f"{pretty_key}: {value}")

            displayed.add(field)

        # Display any remaining metadata
        for key, value in metadata.items():

            if (
                key in displayed
                or value in (None, "", [], {})
            ):
                continue

            pretty_key = key.replace("_", " ").title()

            lines.append(f"{pretty_key}: {value}")

        lines.extend([
            "",
            "Content:",
            content,
        ])

        formatted_documents.append("\n".join(lines))

    return separator.join(formatted_documents)


def main():

    question = input("Enter your question: ").strip()

    if not question:
        print("Question cannot be empty.")
        return

    documents = retrieve_documents(question)

    context = format_documents(documents)

    print("\n" + "=" * 80)
    print("Retrieved Context")
    print("=" * 80)

    print(f"\nQuestion:\n{question}")

    print("\nContext:\n")
    print(context)


if __name__ == "__main__":
    main()