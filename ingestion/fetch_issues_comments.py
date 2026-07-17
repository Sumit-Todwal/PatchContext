from ingestion.github_client import GitHubClient

from utils.file_utils import (
    load_json,
    save_json
)

from utils.logger import logger

from config import (
    ISSUES_FILE,
    ISSUE_COMMENTS_FILE,
    DEVELOPMENT_MODE,
    MAX_ISSUES_TO_PROCESS
)



def main():

    client = GitHubClient()

    issues = load_json(ISSUES_FILE)

    if DEVELOPMENT_MODE:
        issues = issues[:MAX_ISSUES_TO_PROCESS]

    logger.info(
        f"Loaded {len(issues)} issues."
    )

    all_comments = []

    for issue in issues:

        try:

            comments = client.get_by_url(
                issue["comments_url"]
            )

            for comment in comments:

                processed_comment = {

                    "id": comment["id"],

                    "type": "issue_comment",

                    "issue_number": issue["number"],

                    "author": (
                        comment["user"]["login"]
                        if comment["user"]
                        else "Unknown"
                    ),

                    "created_at": comment["created_at"],

                    "body": comment["body"],

                    "url": comment["html_url"]
                }

                all_comments.append(
                    processed_comment
                )

        except Exception as e:

            logger.error(
                f"Issue #{issue['number']} failed: {e}"
            )

    save_json(
        all_comments,
        ISSUE_COMMENTS_FILE
    )

    logger.info(
        f"Saved {len(all_comments)} issue comments."
    )


if __name__ == "__main__":
    main()