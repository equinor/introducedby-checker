import xml.etree.ElementTree as ET

class MarkedDependency:
    def __init__(self, name: str, introduced_by:str):
        self.name = name
        self.introduced_by = introduced_by

class Project:
    def __init__(self, name:str, file_path:str): 
        self.name = name
        self.file_path = file_path
        self.marked_dependency = []

    def add_marked_dependency(self, marked_dependency: MarkedDependency):
        self.marked_dependency.append(marked_dependency)
    
    def get_marked_dependencies(self):
        return self.marked_dependency

class Report:
    def __init__(self):
        self.projects = []

    def add_project(self, project: Project):
        self.projects.append(project)

    def get_projects(self):
        return self.projects