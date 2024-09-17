import ast
from utils.file_util import FileUtil

class FunctionInfoVisitor(ast.NodeVisitor):
    def __init__(self):
        self.functions = []
        self.scope_level = 0

    def get_function_signature(self, node):
        if not isinstance(node, ast.FunctionDef):
            return None
        parameters = []
        defaults = [None] * (len(node.args.args) - len(node.args.defaults)) + node.args.defaults
        for arg, default in zip(node.args.args, defaults):
            param_name = arg.arg
            param_annotation = ast.get_source_segment(self.source_code, arg.annotation) if arg.annotation else None
            param_str = f"{param_name}: {param_annotation}" if param_annotation else param_name
            if default:
                param_str += f" = {ast.get_source_segment(self.source_code, default)}"
            parameters.append(param_str)
        
        if node.args.vararg:
            parameters.append(f"*{node.args.vararg.arg}")
        
        for kwonly_arg, kwonly_default in zip(node.args.kwonlyargs, node.args.kw_defaults):
            kwonly_name = kwonly_arg.arg
            kwonly_annotation = ast.get_source_segment(self.source_code, kwonly_arg.annotation) if kwonly_arg.annotation else None
            kwonly_str = f"{kwonly_name}: {kwonly_annotation}" if kwonly_annotation else kwonly_name
            if kwonly_default:
                kwonly_str += f" = {ast.get_source_segment(self.source_code, kwonly_default)}"
            parameters.append(kwonly_str)
        
        if node.args.kwarg:
            parameters.append(f"**{node.args.kwarg.arg}")
        
        return_annotation = ast.get_source_segment(self.source_code, node.returns) if node.returns else None
        if return_annotation:
            signature = f"def {node.name}({', '.join(parameters)}) -> {return_annotation}:"
        else:
            signature = f"def {node.name}({', '.join(parameters)}):"
        
        return signature



    def visit_FunctionDef(self, node):
        if self.scope_level == 0:
            signature = self.get_function_signature(node)
            docstring = ast.get_docstring(node)
            self.functions.append({
                'name': node.name,
                'source': ast.unparse(node),
                'signature': signature,
                'docstring': docstring,
                'start_lineno': node.lineno,
                'end_lineno': node.end_lineno,
                'class': None
            })
        self.scope_level += 1
        self.generic_visit(node)
        self.scope_level -= 1

    def visit_ClassDef(self, node):
        self.scope_level += 1
        for sub_node in node.body:
            if isinstance(sub_node, ast.FunctionDef):
                signature = self.get_function_signature(sub_node)
                docstring = ast.get_docstring(sub_node)
                self.functions.append({
                    'name': sub_node.name,
                    'source': ast.unparse(sub_node),
                    'signature': signature,
                    'docstring': docstring,
                    'start_lineno': sub_node.lineno,
                    'end_lineno': sub_node.end_lineno,
                    'class': node.name
                })
        self.generic_visit(node)
        self.scope_level -= 1

def extract_function_info(file_path):
    source_code = FileUtil.read_py_file(file_path)
    tree = ast.parse(source_code)

    function_info_visitor = FunctionInfoVisitor()
    function_info_visitor.source_code = source_code  
    function_info_visitor.visit(tree)

    return function_info_visitor.functions

def extract_function_info_from_source_code(source_code):
    tree = ast.parse(source_code)

    function_info_visitor = FunctionInfoVisitor()
    function_info_visitor.source_code = source_code  
    function_info_visitor.visit(tree)

    return function_info_visitor.functions



