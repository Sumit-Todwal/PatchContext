from ingestion.github_client import GitHubClient

from utils.file_utils import (
    load_json,
    save_json
)

from utils.logger import logger

from config import (
    PRS_FILE,
    PR_COMMENTS_FILE,
    DEVELOPMENT_MODE,
    MAX_PRS_TO_PROCESS
)


def main():

    client = GitHubClient()

    pull_requests = load_json(PRS_FILE)

    if DEVELOPMENT_MODE:
        pull_requests = pull_requests[:MAX_PRS_TO_PROCESS]

    logger.info(f"Loaded {len(pull_requests)} pull requests.")

    all_comments = []

    for pr in pull_requests:

        logger.info(f"Processing PR #{pr['number']}")

        try:
            # Fetch normal discussion comments
            issue_comments = client.get_by_url(
                pr["comments_url"]
            )

            # Fetch code review comments
            review_comments = client.get_by_url(
                pr["review_comments_url"]
            )

        except Exception as e:
            logger.error(
                f"Failed to process PR #{pr['number']}: {e}"
            )
            continue

        # Process issue comments
        for comment in issue_comments:

            processed_comment = {
                "id": comment["id"],
                "type": "pr_comment",
                "comment_type": "issue",
                "pr_number": pr["number"],
                "author": (
                    comment["user"]["login"]
                    if comment["user"]
                    else "Unknown"
                ),
                "created_at": comment["created_at"],
                "body": comment["body"] or "",
                "url": comment["html_url"]
            }

            all_comments.append(processed_comment)

        # Process review comments
        for comment in review_comments:

            processed_comment = {
                "id": comment["id"],
                "type": "pr_comment",
                "comment_type": "review",
                "pr_number": pr["number"],
                "author": (
                    comment["user"]["login"]
                    if comment["user"]
                    else "Unknown"
                ),
                "created_at": comment["created_at"],
                "body": comment["body"] or "",
                "url": comment["html_url"]
            }

            all_comments.append(processed_comment)

    save_json(
        all_comments,
        PR_COMMENTS_FILE
    )

    logger.info(
        f"Saved {len(all_comments)} PR comments."
    )


if __name__ == "__main__":
    main()

