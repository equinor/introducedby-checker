import xml.etree.ElementTree as ET
import os
from findings import Findings, PackageReference, Project

class ProjectFileEditor:
    
    @staticmethod
    def scan_and_delete_marked_package_references(findings: Findings) -> None:
        project_files = ProjectFileEditor._get_project_file_paths()
        if(len(project_files)<1):
            print("No project files found")
            
        for f in project_files:
            tree = ET.parse(f)
            root = tree.getroot()
            marked_elements = root.findall("./ItemGroup/PackageReference[@IntroducedBy]")

            if len(marked_elements) >= 1:
                ProjectFileEditor._delete_marked(f, tree, root, marked_elements)
                project = ProjectFileEditor._map_marked_to_project(f, marked_elements)
                findings.add_project(project)

    @staticmethod
    def _get_project_file_paths() -> []:
        return [
             os.path.join(root, file)
             for root, files in os.walk(os.getcwd()) 
             for file in files 
             if file.endswith('.csproj') or file.endswith('fsproj')
             ]

    @staticmethod  
    def _delete_marked(f: str, tree: ET.ElementTree, root: ET.Element, elements: list[ET.Element]) -> None:
        parent = root.find("./ItemGroup/PackageReference[@IntroducedBy]/..")
        for e in elements:
            parent.remove(e)
        tree.write(f)

    @staticmethod
    def _map_marked_to_project(f: str, elements: list[ET.Element]) -> Project:
        project = Project(os.path.basename(f), f)

        for e in elements:
            package_ref = PackageReference(
                name = f"{e.attrib.get('Include')}@{e.attrib.get('Version')}",
                introduced_by = e.attrib.get("IntroducedBy")
                )
            project.add_package_reference(package_ref)
            
        return project