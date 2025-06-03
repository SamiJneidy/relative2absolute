import os
import re

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

def process_module(path_list: list[str]) -> None:
    """Converts relative imports in a python module to absolute imports"""
    try:
        file_path = os.path.join(*path_list)
    except FileNotFoundError as e:
        raise e
    
    with open(file_path, 'r', encoding='utf-8') as file:
        # The new content of the module after modifying imports
        new_content = ""
        # Loop over the lines of the module
        for line in file:
            height = get_relative_import_height(line)
            # This is not an import statement
            if height == -1:
                new_content += line
            # This is an import statemtn, modify it
            else:
                # Replace the dots with the corresponding path from the path list.
                # Start from the root, taking the first 'height' elements of the path list
                end = len(path_list) - height
                path = ".".join(path_list[:end])
                new_line = re.sub(r'^from (\.+)', f'from {path}.', line)   
                new_content += new_line

    # Write the new content
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(new_content)

def process_package(path_list: list[str]) -> None:
    """Converts relative imports in a python package and its child packages to absolute imports recusively"""
    try:
        path = os.path.join(*path_list)
    except FileNotFoundError as e:
        raise e
    
    for item in os.listdir(path):
        full_path = os.path.join(path, item)
        # If the current item in the package is a python module modify it directly
        if os.path.isfile(full_path) and item.endswith('.py'):
            path_list.append(item)
            process_module(path_list)
            path_list.pop()
        # Else, the current item is a package so call process_package recursively 
        elif os.path.isdir(full_path):
            path_list.append(item)
            process_package(path_list)
            path_list.pop()

def convert_imports(root_package: str) -> None:
    """Main method to convert imports within a package"""
    try:
        process_package([root_package])
    except Exception as e:
        raise e
    