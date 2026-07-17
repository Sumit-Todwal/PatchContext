from ingestion.github_client import GitHubClient
from utils.file_utils import save_json, load_json

from config import (
    REPO_OWNER,
    REPO_NAME,
    PRS_FILE
)



from utils.logger import logger

def main():
    client = GitHubClient()

    endpoint = f"/repos/{REPO_OWNER}/{REPO_NAME}/pulls"

    pull_requests = client.get_paginated(
        endpoint,
        params={
            "state": "closed"
        }
    )

    logger.info(f"Fetched {len(pull_requests)} pull requests.")

    processed_pull_requests = []

    for pull_request in pull_requests:

        processed_pull_request = {
            "type": "pull_request",
            "number": pull_request["number"],
            "title": pull_request["title"],
            "body": pull_request["body"],
            "state": pull_request["state"],
            "created_at": pull_request["created_at"],
            "merged_at": pull_request["merged_at"],
            "author": (
                pull_request["user"]["login"]
                if pull_request["user"]
                else "Unknown"
            ),
            "url": pull_request["html_url"],


            "comments_url": pull_request["comments_url"],
            "review_comments_url": pull_request["review_comments_url"],
            "merge_commit_sha": pull_request["merge_commit_sha"]
        }

        processed_pull_requests.append(processed_pull_request)


    save_json(
        processed_pull_requests,
        PRS_FILE
    )

    logger.info(f"Saved {len(processed_pull_requests)} pull requests.")

if __name__ == "__main__":
    main()