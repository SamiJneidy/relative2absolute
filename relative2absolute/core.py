from dataclasses import dataclass
import os
import re

@dataclass
class NewFile:
    """This is the schema for saving files temporarly to apply the changes later if no exception was raised during the process"""
    file_path: str
    content: str

def get_relative_import_height(import_statement: str) -> int:
    """
    Returns the height of the module or package we're importing from (the number of dots '.' in the begging of the import statement)
    It returns -1 in case the passed statement does not start with 'from .'.
    For example, if we have the following import statement: 'from ...app.utils import mail' it returns 3 
    """
    if not import_statement.startswith("from ."):
        return -1
    cnt = 0
    for i in import_statement:
        if i == '.':
            cnt+=1
        elif cnt > 0:
            break
    return cnt

def process_module(package_path: list[str], root_path: str, changes: list[NewFile]) -> None:
    """Converts relative imports in a python module to absolute imports"""
    try:
        file_path = os.path.normpath(root_path)
    except FileNotFoundError as e:
        raise e
    
    with open(file_path, 'r', encoding='utf-8') as file:
        # The new content of the module after modifying imports
        new_content = ""
        # Loop over the lines of the module
        for i, line in enumerate(file):
            height = get_relative_import_height(line)
            # This is not an import statement
            if height == -1:
                new_content += line
            # This is an import statemtn, modify it
            else:
                # Replace the dots with the corresponding path from the path list.
                # Start from the root, taking the first 'height' elements of the path list
                if len(package_path) < height:
                    raise ValueError(f"Too many dots in relative import in module: '{os.path.basename(file_path)}' line {i+1}: '{line.strip()}'")
                end = len(package_path) - height
                path = ".".join(package_path[:end])
                new_line = re.sub(r'^from (\.+)', f'from {path}.', line)   
                new_content += new_line

    # Add the file to the changes list to save changes later
    changes.append(NewFile(file_path, new_content))


def process_package(package_path: list[str], root_path: str, changes: list[NewFile]) -> None:
    """Converts relative imports in a python package and its child packages to absolute imports recusively"""
    try:
        current_package = os.path.normpath(root_path)
    except FileNotFoundError as e:
        raise e
    
    for item in os.listdir(current_package):
        item_path = os.path.join(root_path, item)
        # If the current item in the package is a python module process it directly
        if os.path.isfile(item_path) and item.endswith('.py'):
            package_path.append(item)
            process_module(package_path, item_path, changes)
            package_path.pop()
        # If the current item in the package is a child package process it recursively
        elif os.path.isdir(item_path):
            package_path.append(item)
            process_package(package_path, item_path, changes)
            package_path.pop()


def convert_imports(root: str) -> None:
    """Main method to convert imports within a package"""
    root_path = os.path.normpath(root)
    try:
        root_package = os.path.basename(root_path)
        changes: list[NewFile] = []
        process_package(package_path=[root_package], root_path=root_path, changes=changes)
        # Save the changes
        for file in changes:    
            with open(file.file_path, 'w', encoding='utf-8') as new_file:
                new_file.write(file.content)
    except Exception as e:
        raise e
    