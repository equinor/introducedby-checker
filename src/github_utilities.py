from github import Github, Issue, Auth, Repository
from report import DependencyReport

class DependencyReportPublisher:

    @staticmethod
    def publish_report(repo: Repository, report: DependencyReport):
        return