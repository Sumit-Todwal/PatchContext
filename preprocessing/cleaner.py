from utils.file_utils import (
    load_json,
    save_json
)

from utils.logger import logger

from config import (
    DOCUMENTS_FILE,
    CLEAN_DOCUMENTS_FILE
)


def is_empty(document):
    return len(document["text"].strip()) == 0


def is_release_note(document):
    text = document["text"].lower()

    keywords = [
        "release notes",
        "update release notes",
        "[skip ci]"
    ]

    return any(keyword in text for keyword in keywords)


def is_dependency_update(document):
    text = document["text"].lower()

    keywords = [
        "dependabot",
        "bump ",
        "bump the ",
        "bump github-actions",
        "typing-extensions",
        "pre-commit hooks",
        "requirements.txt"
    ]

    return any(keyword in text for keyword in keywords)


def is_too_short(document):
    return len(document["text"].split()) < 10


def clean_documents(documents):

    cleaned_documents = []

    seen = set()

    stats = {
        "empty": 0,
        "release_notes": 0,
        "dependency_updates": 0,
        "duplicates": 0,
        "too_short": 0
    }

    for document in documents:

        if is_empty(document):
            stats["empty"] += 1
            continue

        if is_release_note(document):
            stats["release_notes"] += 1
            continue

        if is_dependency_update(document):
            stats["dependency_updates"] += 1
            continue

        if is_too_short(document):
            stats["too_short"] += 1
            continue

        text = document["text"].strip().lower()

        if text in seen:
            stats["duplicates"] += 1
            continue

        seen.add(text)

        cleaned_documents.append(document)

    return cleaned_documents, stats


def main():

    logger.info("Loading normalized documents...")

    documents = load_json(DOCUMENTS_FILE)

    logger.info(f"Loaded {len(documents)} documents.")

    cleaned_documents, stats = clean_documents(documents)

    save_json(
        cleaned_documents,
        CLEAN_DOCUMENTS_FILE
    )

    logger.info("Cleaning Summary")
    logger.info("-" * 40)

    logger.info(f"Empty Documents      : {stats['empty']}")
    logger.info(f"Release Notes        : {stats['release_notes']}")
    logger.info(f"Dependency Updates   : {stats['dependency_updates']}")
    logger.info(f"Short Documents      : {stats['too_short']}")
    logger.info(f"Duplicates           : {stats['duplicates']}")

    logger.info("-" * 40)

    logger.info(f"Final Documents      : {len(cleaned_documents)}")


if __name__ == "__main__":
    main()