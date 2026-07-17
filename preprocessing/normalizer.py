def normalize_commit(commit):
    """
    Normalize a commit into a common document format.
    """

    return {
        "id": f"commit_{commit['sha']}",
        "type": "commit",
        "text": commit["message"],
        "metadata": {
            "type": "commit",
            "author": commit["author"],
            "created_at": commit["date"],
            "url": commit["url"],
            "sha": commit["sha"],
        },
    }




def normalize_pull_request(pull_request):
    """
    Normalize a pull request into a common document format.
    """

    text = (
        f"Pull Request #{pull_request['number']}\n\n"
        f"Title: {pull_request['title']}\n\n"
        f"Description:\n{pull_request['body'] or ''}"
    )

    return {
        "id": f"pr_{pull_request['number']}",
        "type": "pull_request",
        "text": text,
        "metadata": {
            "type": "pull_request",
            "number": pull_request["number"],
            "title": pull_request["title"],
            "author": pull_request["author"],
            "state": pull_request["state"],
            "created_at": pull_request["created_at"],
            "merged_at": pull_request["merged_at"],
            "url": pull_request["url"],
        },
    }


def normalize_issue(issue):
    """
    Normalize an issue into a common document format.
    """

    text = (
        f"Issue #{issue['number']}\n\n"
        f"Title: {issue['title']}\n\n"
        f"Description:\n{issue['body'] or ''}"
    )

    return {
        "id": f"issue_{issue['number']}",
        "type": "issue",
        "text": text,
        "metadata": {
            "type": "issue",
            "number": issue["number"],
            "title": issue["title"],
            "author": issue["author"],
            "state": issue["state"],
            "created_at": issue["created_at"],
            "closed_at": issue["closed_at"],
            "url": issue["url"],
        },
    }


def normalize_pr_comment(comment):
    """
    Normalize a pull request comment into a common document format.
    """

    text = (
        f"Pull Request #{comment['pr_number']}\n\n"
        f"{comment['comment_type'].capitalize()} Comment\n\n"
        f"{comment['body']}"
    )

    return {
        "id": f"pr_comment_{comment['id']}",
        "type": "pr_comment",
        "text": text,
        "metadata": {
            "type": "pr_comment",
            "author": comment["author"],
            "created_at": comment["created_at"],
            "url": comment["url"],
            "pr_number": comment["pr_number"],
            "comment_type": comment["comment_type"],
        },
    }


def normalize_issue_comment(comment):
    """
    Normalize an issue comment into a common document format.
    """

    text = (
        f"Issue #{comment['issue_number']}\n\n"
        f"Comment\n\n"
        f"{comment['body']}"
    )

    return {
        "id": f"issue_comment_{comment['id']}",
        "type": "issue_comment",
        "text": text,
        "metadata": {
            "type": "issue_comment",
            "author": comment["author"],
            "created_at": comment["created_at"],
            "url": comment["url"],
            "issue_number": comment["issue_number"],
        },
    }