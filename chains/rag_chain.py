from retrieval.retriever import (
    retrieve_documents,
    format_documents,
)

from prompts.rag_prompt import RAG_PROMPT
from models.llm import get_llm
from utils.logger import logger


# Load the LLM once
llm = get_llm()


def extract_sources(documents):
    """
    Extract unique sources from retrieved documents.
    """

    sources = []
    seen = set()

    for document in documents:

        metadata = document.metadata

        source_type = metadata.get("type", document.metadata.get("source", "Unknown"))

        url = metadata.get("url")

        # Build readable labels
        if source_type == "pull_request":
            label = f"Pull Request #{metadata.get('number')}"

        elif source_type == "issue":
            label = f"Issue #{metadata.get('number')}"

        elif source_type == "commit":
            sha = metadata.get("sha", "")
            label = f"Commit {sha[:7]}"

        elif source_type == "pr_comment":
            label = f"PR #{metadata.get('pr_number')} Comment"

        elif source_type == "issue_comment":
            label = f"Issue #{metadata.get('issue_number')} Comment"

        else:
            label = source_type.replace("_", " ").title()

        key = (label, url)

        if key in seen:
            continue

        seen.add(key)

        sources.append(
            {
                "type" : source_type,
                "label": label,
                "url": url,
            }
        )

    return sources


def generate_answer(question: str) -> dict:
    """
    Generate an answer using Retrieval-Augmented Generation.
    """

    logger.info(f"Question: {question}")

    logger.info("Retrieving relevant documents...")

    documents = retrieve_documents(question)

    context = format_documents(documents)

    logger.info("Generating answer...")

    prompt = RAG_PROMPT.invoke(
        {
            "context": context,
            "question": question,
        }
    )

    response = llm.invoke(prompt)

    logger.info("Answer generated successfully.")

    return {
        "answer": response.content,
        "sources": extract_sources(documents),
    }


def main():

    print("=" * 80)
    print("PatchContext")
    print("=" * 80)

    while True:

        question = input("\nAsk a question ('exit' to quit): ").strip()

        if question.lower() == "exit":
            break

        if not question:
            continue

        result = generate_answer(question)

        print("\n" + "=" * 80)
        print("Answer")
        print("=" * 80)

        print(result["answer"])

        print("\n" + "=" * 80)
        print("Sources")
        print("=" * 80)

        for source in result["sources"]:
            print(f"- {source['label']}")

            if source["url"]:
                print(f"  {source['url']}")

            print()


if __name__ == "__main__":
    main()