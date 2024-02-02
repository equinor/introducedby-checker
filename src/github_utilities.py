from github import Repository, InputGitAuthor
from datetime import date
from report import Report, Project
from md_table_builder import MarkdownTableBuilder


class PullRequestCreator:
    def __init__(self, repo: Repository, report : Report, base_name: str):
        self.repo = repo
        self.report = report
        self.base_name = base_name
        self.base_branch = repo.get_branch(base_name)
        self.target_branch = f'introducedby-checker/{date.today()}'

    def create_pull_request(self):
        self.create_branch()
        for p in self.report.get_projects():
            self.push(p)
        self.repo.create_pull(base="main", head=self.target_branch, title = f"🤖IntroducedBy Checker {date.today()}🤖", body = self.create_body())

    def create_branch(self):
        self.repo.create_git_ref(ref='refs/heads/' + self.target_branch, sha=self.base_branch.commit.sha)

    def push(self, p: Project):
        author = InputGitAuthor(
        "GitHub Action",
        "action@github.com")
        commit_message = f"Deleting marked package references from {p.name}"
        with open(p.file_path) as f: new_file_content = f.read()
        contents = self.repo.get_contents("TestProject/TestProject.csproj", ref=self.target_branch)
        self.repo.update_file(contents.path, commit_message, new_file_content, contents.sha, branch = self.target_branch, author = author)
        
    def create_body(self):
        body = ""
        for p in self.report.get_projects():
            body+=f"## {p.name}\n"
            table = MarkdownTableBuilder()
            for m in p.get_marked_dependencies():
                table.add_row([m.name, m.introduced_by])
            body+=str(table)
            body+="\n"
        return body