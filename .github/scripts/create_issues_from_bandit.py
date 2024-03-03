import json
import sys
from github import Github
import os

# Initialize GitHub client
g = Github(sys.argv[1])
repo = g.get_repo(sys.argv[2])


def issue_exists(title):
    open_issues = repo.get_issues(state='open')
    for issue in open_issues:
        if issue.title == title:
            return True
    return False


def create_issue(title, body):
    if not issue_exists(title):
        repo.create_issue(title=title, body=body)
        print(f"Issue created: {title}")
    else:
        print(f"Issue already exists and was not created: {title}")


def main():
    # Construct the absolute path for 'bandit-results.json'
    current_script_path = os.path.dirname(os.path.abspath(__file__))
    results_file_path = os.path.join(current_script_path, '..', 'bandit-results.json')

    with open(results_file_path) as f:
        data = json.load(f)

    for result in data['results']:
        title = f"[Bandit] {result['test_id']}: {result['issue_text']}"
        body = f"""
## Issue Description
- **Test ID**: {result['test_id']}
- **Issue**: {result['issue_text']}
- **Severity**: {result['issue_severity']}
- **Confidence**: {result['issue_confidence']}
- **File**: {result['filename']}
- **Line**: {result['line_number']}
- **Code**: 
```python
{result['code']}
"""
