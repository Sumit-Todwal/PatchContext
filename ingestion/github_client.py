import os
import time
import requests
from dotenv import load_dotenv
from utils.logger import logger
from config import (
    REQUEST_TIMEOUT,
    MAX_RETRIES,
    RETRY_DELAY
)

load_dotenv()

class GitHubClient():

    def __init__(self):
        self.base_url = "https://api.github.com"
        self.token = os.getenv("GITHUB_TOKEN")
        self.headers = {
            "Authorization" : f"Bearer {self.token}",
            "Accept" : "application/vnd.github+json",
            "User-Agent" : "PatchContext"
        }
        self.session = requests.Session()
        self.session.headers.update(self.headers)

    def get(self, endpoint, params=None):

        url = f"{self.base_url}{endpoint}"

        response = self._request_with_retry(
            url,
            params
        )

        return response.json()
    

    def get_paginated(self, endpoint, params=None):
        """
        Fetch all pages from a paginated GitHub endpoint.
        """

        if params is None:
            params = {}

        params["per_page"] = 100

        page = 1
        all_results = []

        while True:

            params["page"] = page

            data = self.get(endpoint, params=params)

            if not data:
                break

            all_results.extend(data)

            logger.info(
                f"Fetched page {page} ({len(data)} records)"
            )

            page += 1

        return all_results
    
    def _request_with_retry(self, url, params=None):

        for attempt in range(1, MAX_RETRIES + 1):

            try:

                logger.info(
                    f"Attempt {attempt}: GET {url}"
                )

                response = self.session.get(
                    url,
                    params=params,
                    timeout=REQUEST_TIMEOUT
                )

                logger.info(
                    f"Status Code: {response.status_code}"
                )

                response.raise_for_status()

                return response

            except requests.exceptions.RequestException as e:

                logger.warning(
                    f"Attempt {attempt} failed: {e}"
                )

                if attempt == MAX_RETRIES:
                    logger.error(
                        "Maximum retries exceeded."
                    )
                    raise

                logger.info(
                    f"Retrying in {RETRY_DELAY} seconds..."
                )

                time.sleep(RETRY_DELAY)

    def get_by_url(self, url, params=None):
        """
        Fetch data using a complete GitHub API URL.
        """

        response = self._request_with_retry(
            url,
            params
        )
        
        return response.json()





if __name__ == "__main__":
    client = GitHubClient()

    repo = client.get("/repos/fastapi/fastapi")

    print(repo["name"])
    print(repo["description"])
    print(repo["stargazers_count"])
