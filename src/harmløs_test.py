from github import Github
import requests
import base64
import json 

def commit(github: Github, token: str):

    repo_uri = "equinor/introducedby-checker"
    repo = github.get_repo(repo_uri)

    repo_name = repo.name 
    repo_org = repo.organization.name 
    file_path = "src/test_file.txt"
    target_branch = "test_signed_commits" 
    file_sha = repo.get_contents(file_path, target_branch).sha
    commit_message = "Test commit, pls be verified"

    commit_file = open("src/test_file.txt", "rb")
    with open("src/test_file.txt", "rb") as commit_file:
        file_content = commit_file.read()
    encoded_content = base64.b64encode(file_content).decode('utf-8')

    url = f"https://api.github.com/repos/{repo_org}/{repo_name}/contents/{file_path}"
    headers = {
        f"Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3+json"
    }
    data = {
        "message": f"{commit_message}",
        "content": f"{encoded_content}",
        "branch": f"{target_branch}",
        "sha": f"{file_sha}"
    }

    response = requests.put(url, headers=headers, data=json.dumps(data))
    print(response.status_code)
    print(response.json)

