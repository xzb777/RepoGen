import ast
# from utils.file_util import FileUtil


# 定义一个AST节点访问器类，用于访问所有的变量名
class VariableVisitor(ast.NodeVisitor):
    class_a = 1
    def __init__(self, file_path):
        self.current_class = None
        self.variables = []  # 初始化变量列表
        self.file_path = file_path
    def visit_ClassDef(self, node):
        # 记录当前类名
        self.current_class = node.name
        self.generic_visit(node)
        self.current_class = None

    def visit_Assign(self, node):
        # 获取当前赋值语句所在的行号范围
        start_line = node.lineno
        end_line = node.end_lineno

        # 获取多行变量定义的代码块
        variable_lines = []
        with open(self.file_path, 'r', encoding='utf-8') as file:
            lines = file.readlines()
            for line_number in range(start_line, end_line + 1):
                if 1 <= line_number <= len(lines):
                    line_content = lines[line_number - 1].strip()
                    variable_lines.append(line_content)

        # 处理赋值语句，提取变量名
        for target in node.targets:
            if isinstance(target, ast.Name):
                variable_name = target.id
                self.variables.append((variable_name, variable_lines, self.current_class))
        self.generic_visit(node)

    def visit_FunctionDef(self, node):
        # 如果遇到函数定义，不继续遍历函数体内的内容，直接跳过
        pass

def get_variables_from_file(file_path):
    dict_variables = {}
    source_code = ""
    with open(file_path, 'r', encoding='utf-8') as file:
        # 去除BOM字符
        source_code = file.read().lstrip('\ufeff')

    # 解析代码为AST
    tree = ast.parse(source_code)
    # 创建访问器并遍历AST
    visitor = VariableVisitor(file_path)
    visitor.visit(tree)

    all_variables = visitor.variables
    for var, lines, class_name in all_variables:
        if class_name:
            if class_name in dict_variables:
                dict_variables[class_name].extend(lines)
            else:
                dict_variables[class_name] = lines
        else:
            if 'module' in dict_variables:
                dict_variables['module'].extend(lines)
            else:
                dict_variables['module'] = lines

    return dict_variables



if __name__ == "__main__":
    file_path = "/home/gudako/repo/repogen/lib/a3/utils/LocalInfoExtractor.py"
    vd = get_variables_from_file(file_path)
    print(vd)



