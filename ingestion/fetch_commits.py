import json
import os
from ingestion.github_client import GitHubClient
from utils.file_utils import save_json, load_json

def main():
    client = GitHubClient()

    commits = client.get("/repos/fastapi/fastapi/commits", params={"per_page" : 10})

    print(f"Fetched {len(commits)} commits.\n")

    print(json.dumps(commits[0], indent=4))


    processed_commits = []

    for commit in commits:
        processed_commit = {
            "type": "commit",
            "sha": commit["sha"],
            "author": commit["commit"]["author"]["name"],
            "date": commit["commit"]["author"]["date"],
            "message": commit["commit"]["message"],
            "url": commit["html_url"]
        }

        processed_commits.append(processed_commit)


    os.makedirs("data/raw", exist_ok=True)

    save_json(
        processed_commits,
        "data/raw/commits.json"
    )

if __name__ == "__main__":
    main()