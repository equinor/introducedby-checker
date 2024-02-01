import xml.etree.ElementTree as ET
import os
from report import Report, MarkedDependency, Project

class ProjectFileEditor:

    def scan_and_delete_marked_package_references(report: Report):
        project_files = ProjectFileEditor._get_project_file_paths()
        for f in project_files:
            tree = ET.parse(f)
            root = tree.getroot()
            marked_deps = root.findall("./ItemGroup/PackageReference[@IntroducedBy]")
            if marked_deps is not None:
                ProjectFileEditor._delete_marked_package_references(f, tree, root, marked_deps)

                project = ProjectFileEditor._add_marked_dependency_to_project(f, marked_deps)
                report.add_project(project)

    def _get_project_file_paths():
        return [
             os.path.join(root, file)
             for root, dirs, files in os.walk(os.getcwd()) 
             for file in files 
             if file.endswith('.csproj') or file.endswith('fsproj')
             ]
    
    def _add_marked_dependency_to_project(f: str, deps: []):
        project = Project(os.path.basename(f), f)
        print(project.name)
        print(project.file_path)
        for d in deps:
            marked_dependency = MarkedDependency(
                name = f"{d.attrib.get('Include')}@{d.attrib.get('Version')}",
                introduced_by = d.attrib.get("BecauseOf"))
            project.add_marked_dependency(marked_dependency)
        return project
        
    def _delete_marked_package_references(f: str, tree: ET.ElementTree, root: ET.Element, marked_deps: list[ET.Element]):
        parent = root.find("./ItemGroup/PackageReference[@IntroducedBy]/..")
        for m in marked_deps:
            parent.remove(m)
        tree.write(f)