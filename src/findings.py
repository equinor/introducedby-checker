class PackageReference:
    def __init__(self, name: str, introduced_by:str):
        self.name = name
        self.introduced_by = introduced_by

class Project:
    def __init__(self, name:str, file_path:str): 
        self.name = name
        self.file_path = file_path
        self.package_references = []

    def add_package_reference(self, dependency: PackageReference):
        self.package_references.append(dependency)

    def get_package_references(self):
        return self.package_references

class Findings:
    def __init__(self):
        self.projects = []

    def add_project(self, project: Project):
        self.projects.append(project)

    def get_projects(self):
        return self.projects