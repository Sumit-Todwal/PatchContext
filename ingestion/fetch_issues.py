from ingestion.github_client import GitHubClient
from utils.file_utils import save_json, load_json

from config import (
    REPO_OWNER,
    REPO_NAME,
    ISSUES_FILE
)

from utils.logger import logger



def main():
    client = GitHubClient()

    endpoint = f"/repos/{REPO_OWNER}/{REPO_NAME}/issues"

    issues = client.get_paginated(
        endpoint,
        params={
            "state": "closed"
        }
    )

    logger.info(f"Fetched {len(issues)} items from Issues API.")

    processed_issues = []

    for issue in issues:

        if "pull_request" in issue:
            continue

        processed_issue = {
            "type": "issue",
            "number": issue["number"],
            "title": issue["title"],
            "body": issue["body"],
            "state": issue["state"],
            "created_at": issue["created_at"],
            "closed_at": issue["closed_at"],
            "author": (
                issue["user"]["login"]
                if issue["user"]
                else "Unknown"
            ),
            "url": issue["html_url"],

            # We'll use this later in fetch_issue_comments.py
            "comments_url": issue["comments_url"]
        }

        processed_issues.append(processed_issue)

    save_json(
        processed_issues,
        ISSUES_FILE
    )

    logger.info(f"Saved {len(processed_issues)} issues.")


if __name__ == "__main__":
    main()