import os
import ast
import logging
from typing import List, Tuple, Optional, Dict

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

class VariableVisitor(ast.NodeVisitor):
    def __init__(self, file_path):
        self.current_class = None
        self.variables = []  
        self.init_methods = []  
        self.file_path = file_path

    def visit_ClassDef(self, node):
        self.current_class = node.name
        for item in node.body:
            if isinstance(item, ast.Assign):
                self._process_assign(item, is_class_var=True)
            elif isinstance(item, ast.AnnAssign):
                self._process_annotated_assign(item, is_class_var=True)
            elif isinstance(item, ast.FunctionDef):
                if item.name == '__init__':
                    self._process_init(item)
                for subitem in item.body:
                    if isinstance(subitem, ast.Assign):
                        self._process_assign(subitem, is_class_var=False)
                    elif isinstance(subitem, ast.AnnAssign):
                        self._process_annotated_assign(subitem, is_class_var=False)
        self.generic_visit(node)
        self.current_class = None
    def visit_Assign(self, node):
        if self.current_class is None:
            self._process_assign(node, is_class_var=False)

    def visit_AnnAssign(self, node):
        if self.current_class is None:
            self._process_annotated_assign(node, is_class_var=False)

    def _process_assign(self, node, is_class_var: bool):
        start_line = node.lineno
        end_line = node.end_lineno
        variable_lines = []
        with open(self.file_path, 'r', encoding='utf-8') as file:
            lines = file.readlines()
            for line_number in range(start_line, end_line + 1):
                if 1 <= line_number <= len(lines):
                    line_content = lines[line_number - 1].strip()
                    variable_lines.append(line_content)
        for target in node.targets:
            if isinstance(target, ast.Name):
                variable_name = target.id
                var_type = 'class_variable' if is_class_var else 'instance_variable'
                self.variables.append((variable_name, variable_lines, self.current_class, var_type))

    def _process_annotated_assign(self, node, is_class_var: bool):
        start_line = node.lineno
        end_line = node.end_lineno
        variable_lines = []
        with open(self.file_path, 'r', encoding='utf-8') as file:
            lines = file.readlines()
            for line_number in range(start_line, end_line + 1):
                if 1 <= line_number <= len(lines):
                    line_content = lines[line_number - 1].strip()
                    variable_lines.append(line_content)
        if isinstance(node.target, ast.Name):
            variable_name = node.target.id
            var_type = 'class_variable' if is_class_var else 'instance_variable'
            self.variables.append((variable_name, variable_lines, self.current_class, var_type))

    def _process_init(self, node):
        start_line = node.lineno
        end_line = node.end_lineno

        init_lines = []
        with open(self.file_path, 'r', encoding='utf-8') as file:
            lines = file.readlines()
            for line_number in range(start_line, end_line + 1):
                if 1 <= line_number <= len(lines):
                    line_content = lines[line_number - 1].strip()
                    init_lines.append(line_content)

        self.init_methods.append((self.current_class, init_lines))

    def visit_FunctionDef(self, node):
        pass

def get_variables_from_file(file_path: str):
    dict_variables = {}
    source_code = ""
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            source_code = file.read().lstrip('\ufeff')
        tree = ast.parse(source_code)
        visitor = VariableVisitor(file_path)
        visitor.visit(tree)
        all_variables = visitor.variables
        for var, lines, class_name, var_type in all_variables:
            class_name = class_name if class_name else 'module'
            if class_name not in dict_variables:
                dict_variables[class_name] = {'class_variables': [], 'instance_variables': []}
            
            if var_type == 'class_variable':
                dict_variables[class_name]['class_variables'].append((var, lines))
            elif var_type == 'instance_variable':
                dict_variables[class_name]['instance_variables'].append((var, lines))

        for class_name, init_lines in visitor.init_methods:
            if class_name not in dict_variables:
                dict_variables[class_name] = {'class_variables': [], 'instance_variables': [], 'init_method': []}
            dict_variables[class_name]['init_method'] = init_lines

    except SyntaxError as e:
        logger.error("Syntax error while parsing the file %s: %s", file_path, e)
    except Exception as e:
        logger.error("Error while processing the file %s: %s", file_path, e)

    return dict_variables

def traverse_directory(directory: str):
    all_files_variables = {}
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith('.py'):
                file_path = os.path.join(root, file)
                file_variables = get_variables_from_file(file_path)
                all_files_variables[file_path] = file_variables
    return all_files_variables


def get_class_variables_for_fqn(all_files_variables, fqn: str):
    for file_path, file_data in all_files_variables.items():
        for class_name, class_data in file_data.items():
            # 检查 class_name 是否是 fqn 的后缀
            if fqn.endswith(class_name):
                return class_data.get('class_variables', [])
    return []


def get_class_variables(repo_path, relative_path, cl):
    des_path = os.path.join(repo_path, relative_path)
    # print(des_path)
    # print(cl)
    all_variables = traverse_directory(repo_path)
    for path, path_dict in all_variables.items():
        for class_name, class_dict in path_dict.items():
            if cl.endswith(class_name) and path == des_path: 
                return class_dict["class_variables"]


