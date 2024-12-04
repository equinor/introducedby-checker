from github import Repository, InputGitAuthor
from datetime import date
from findings import Findings, Project
from io import StringIO
import requests
import base64
import json
from md_table_builder import MarkdownTableBuilder

class PullRequestCreator:
    def __init__(self, repo: Repository, git_token: str, findings: Findings):
        self.repo = repo
        self.git_token = git_token
        self.findings = findings
        self.source = repo.get_branch(repo.default_branch)
        self.target_branch = f'introducedby-checker/{date.today()}'

    def create_pull_request(self) -> None:
        self._create_branch()

        for p in self.findings.get_projects():
            self._commit_changes(p)

        self.repo.create_pull(
            base=self.source.name, 
            head=self.target_branch, 
            title = f"🤖IntroducedBy Checker {date.today()}🤖", 
            body = self._create_body())

    def _create_branch(self) -> None:
        try:
            self.repo.create_git_ref(ref='refs/heads/' + self.target_branch, sha=self.source.commit.sha)
        except:
            raise Exception(f"This is the default branch: {self.repo.default_branch}. The default branch is None: {self.source is None}. The SHA of the last commit from default branch is {self.source.commit.sha}")

    def _commit_changes(self, p: Project) -> None:                
        with open(p.file_path, "rb") as f: new_file_content = f.read()
        encoded_content = base64.b64encode(new_file_content).decode('utf-8')
        file_sha = self.repo.get_contents(p.file_path, ref=self.target_branch).sha
        commit_message = f"Deleting marked package references from {p.name}"
        
        url = f"https://api.github.com/repos/{self.repo.organization.name}/{self.repo.name}/contents/{p.file_path}"
        headers = {
            f"Authorization": f"token {self.git_token}",
            "Accept": "application/vnd.github.v3+json"
            }
        
        data = {
            "message": f"{commit_message}",
            "content": f"{encoded_content}",
            "branch": f"{self.target_branch}",
            "sha": f"{file_sha}"
            }
        
        response = requests.put(url, headers=headers, data=json.dumps(data))
        print(response.status_code)
        print(response.json)
        
    def _create_body(self) -> str:
        body = StringIO()
        body.write("Deleted package references marked with the `IntroducedBy` attribute.")
        body.write("\n")
        for p in self.findings.get_projects():
            body.write(f"## {p.name}\n")
            table = MarkdownTableBuilder()
            for ref in p.get_package_references():
                table.add_row([ref.name, ref.introduced_by])
            body.write(str(table))
            body.write("\n")
        return body.getvalue()