from preprocessing.normalizer import (
    normalize_commit,
    normalize_pull_request,
    normalize_issue,
    normalize_pr_comment,
    normalize_issue_comment
)

from utils.file_utils import (
    load_json,
    save_json
)



from utils.logger import logger

from config import (
    COMMITS_FILE,
    PRS_FILE,
    ISSUES_FILE,
    PR_COMMENTS_FILE,
    ISSUE_COMMENTS_FILE,
    DOCUMENTS_FILE
)


def process_file(filepath, normalize_function):
    """
    Load a JSON file and normalize every record.
    """
    records = load_json(filepath)
    return [normalize_function(record) for record in records]


def build_documents():

    logger.info("Building normalized documents...")

    documents = []

    datasets = [
        (COMMITS_FILE, normalize_commit),
        (PRS_FILE, normalize_pull_request),
        (ISSUES_FILE, normalize_issue),
        (PR_COMMENTS_FILE, normalize_pr_comment),
        (ISSUE_COMMENTS_FILE, normalize_issue_comment),
    ]

    for filepath, normalize_function in datasets:

        logger.info(f"Processing {filepath}")

        normalized_documents = process_file(
            filepath,
            normalize_function
        )

        documents.extend(normalized_documents)

        logger.info(
            f"Added {len(normalized_documents)} documents."
        )

    save_json(
        documents,
        DOCUMENTS_FILE
    )

    logger.info(
        f"Successfully built {len(documents)} normalized documents."
    )


if __name__ == "__main__":
    build_documents()