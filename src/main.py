import os
from project_file_editor import ProjectFileEditor
from github_utilities import PullRequestCreator
from findings import Findings
from github import Github, Auth

if __name__ == '__main__':

    acces_token = os.environ.get('GITHUB_TOKEN')
    repo_uri = os.environ.get('GITHUB_REPOSITORY')

    if(repo_uri is None or acces_token is None):
        raise Exception('Could not find repository')
    token = Auth.Token(acces_token)

    github = Github(auth=token)
    repo = github.get_repo(repo_uri)

    findings = Findings()
    ProjectFileEditor.scan_and_delete_marked_package_references(findings)
    if len(findings.get_projects()) >=1: 
        git_utils = PullRequestCreator(repo, token,  findings)
        git_utils.create_pull_request()