import os
from project_file_editor import ProjectFileEditor
from report import Report
from github_utilities import DependencyReportPublisher
from github import Github, Issue, Auth

if __name__ == '__main__':
    acces_token = os.environ.get('GITHUB_TOKEN')
    repo_uri = os.environ.get('GITHUB_REPOSITORY')
    branch_name = os.environ.get('GITHUB_REF_NAME')
    if(repo_uri is None or acces_token is None or branch_name is None):
        raise Exception('Could not find repository')
    token = Auth.Token(acces_token)

    github = Github(auth=token)
    repo = github.get_repo(repo_uri)
    branch = repo.get_branch(branch_name)

   # Create report object
    report = Report()

    #Scan project to find package references marked with IntroducedBy attribute and delete them
    ProjectFileEditor.scan_and_delete_marked_package_references(report)

    #Publish the report
    DependencyReportPublisher.publish_report(repo, report)
