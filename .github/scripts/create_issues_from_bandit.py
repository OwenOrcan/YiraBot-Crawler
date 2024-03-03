import json
import os
import sys
from github import Github


def issue_exists(repo, title):
    open_issues = repo.get_issues(state='open')
    for issue in open_issues:
        if issue.title == title:
            return True
    return False


def create_issue(repo, title, body):
    if not issue_exists(repo, title):
        repo.create_issue(title=title, body=body)
        print(f"Issue created: {title}")
    else:
        print(f"Issue already exists and was not created: {title}")


def main(token, repo_name):
    g = Github(token)
    repo = g.get_repo(repo_name)

    # Assuming the 'bandit-results.json' file is in the root directory
    results_file_path = 'bandit-results.json'

    with open(results_file_path) as f:
        data = json.load(f)

    for result in data['results']:
        title = f"[Bandit] {result['test_id']}: {result['issue_text']}"
        body = (f"## Issue Description\n"
                f"- **Test ID**: {result['test_id']}\n"
                f"- **Issue**: {result['issue_text']}\n"
                f"- **Severity**: {result['issue_severity']}\n"
                f"- **Confidence**: {result['issue_confidence']}\n"
                f"- **File**: {result['filename']}\n"
                f"- **Line**: {result['line_number']}\n"
                f"- **Code**:\n"
                f"```python\n"
                f"{result['code']}\n"
                f"```\n")
        create_issue(repo, title, body)


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: create_issues_from_bandit.py <GITHUB_TOKEN> <REPOSITORY_FULL_NAME>")
        sys.exit(1)

    github_token = os.getenv('GITHUB_TOKEN')
    repository_full_name = os.getenv('GITHUB_REPOSITORY')

    if not github_token or not repository_full_name:
        print("GitHub token or repository name not found.")
        sys.exit(1)

    main(github_token, repository_full_name)
