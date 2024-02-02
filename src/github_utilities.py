from github import Repository, InputGitAuthor
from datetime import date
from findings import Findings, Project
from io import StringIO
from md_table_builder import MarkdownTableBuilder

class PullRequestCreator:
    def __init__(self, repo: Repository, findings: Findings):
        self.repo = repo
        self.findings = findings
        self.source = repo.get_branch(repo.default_branch)
        self.target_branch = f'introducedby-checker/{date.today()}'

    def create_pull_request(self) -> None:
        self._create_branch()

        for p in self.findings.get_projects():
            self._push(p)

        self.repo.create_pull(
            base=self.source.name, 
            head=self.target_branch, 
            title = f"🤖IntroducedBy Checker {date.today()}🤖", 
            body = self._create_body())

    def _create_branch(self) -> None:
        self.repo.create_git_ref(ref='refs/heads/' + self.target_branch, sha=self.source.commit.sha)

    def _push(self, p: Project) -> None:
        author = InputGitAuthor(
        "GitHub Action",
        "action@github.com")
        commit_message = f"Deleting marked package references from {p.name}"
        with open(p.file_path) as f: new_file_content = f.read()
        contents = self.repo.get_contents(p.file_path, ref=self.target_branch)

        self.repo.update_file(
            contents.path,
            commit_message,
            new_file_content,
            contents.sha,
            branch = self.target_branch,
            author = author)
        
    def _create_body(self) -> str:
        body = StringIO()
        body.write("Deleted package references that was marked with the IntroducedBy attribute. Packages marked with this attribute has been installed directly becuase other dependencies used vulnerable versions of these, hence introducing a transitive vulnerability.")
        for p in self.findings.get_projects():
            body.write(f"## {p.name}\n")
            table = MarkdownTableBuilder()
            for ref in p.get_package_references():
                table.add_row([ref.name, ref.introduced_by])
            body.write(str(table))
            body.write("\n")
        return body.getvalue()