from utils.file_util import FileUtil
import json
import re
from llm_util import LLMUtil
from config import Config
import os
from tqdm import tqdm
import astunparse
import ast

import shutil
import os
import textwrap
import pickle

def load_data(filename):
    with open(filename, 'rb') as file:
        data = pickle.load(file)
    logger.info(f"数据已从 {filename} 加载")
    return data


def save_data(data, filename):
    with open(filename, 'wb') as file:
        pickle.dump(data, file)
    logger.info(f"数据已保存到 {filename}")


def copy_project_structure(src, dest):
    if os.path.exists(dest):
        shutil.rmtree(dest)  # 删除目标文件夹及其内容
    shutil.copytree(src, dest)  # 复制整个文件夹结构


def logger_success(message):
    print(f"SUCCESS: {message}")

# Function to copy project structure
def copy_project_structure(src, dest):
    if os.path.exists(dest):
        shutil.rmtree(dest)
    shutil.copytree(src, dest)

# Read the source code from a file
def read_code(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()

# Write the modified code back to a file
def write_code(file_path, code):
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(code)

def select_model(selected_model, message, temperature=0.3):
    if selected_model == LLMUtil.GPT3_5_TURBO_MODEL_NAME:
        return LLMUtil.ask_gpt3_5turbo(message, temperature)
    elif selected_model == LLMUtil.GPT4_0125_PREVIEW_MODEL_NAME:
        return LLMUtil.ask_gpt_4_preview(message, temperature)
    elif selected_model == LLMUtil.GPT4_MODEL_NAME:
        return LLMUtil.ask_gpt_4_turbo(message, temperature)
    elif selected_model == LLMUtil.GPT3_5_TURBO_16K_MODEL_NAME:
        return LLMUtil.ask_gpt3_5turbo16k(message, temperature)
    else:
        raise ValueError(f"Unsupported model name: {selected_model}")

def adjust_code_indentation(code):
    return textwrap.dedent(code).strip()
    
class FunctionReplacer(ast.NodeTransformer):
    def __init__(self, replacements):
        self.replacements = replacements

    def visit_FunctionDef(self, node):
        function_name = node.name
        if function_name in self.replacements:
            # 确保替换的代码是字符串
            new_functions_code = self.replacements[function_name]
            if not isinstance(new_functions_code, str):
                raise ValueError(f"Expected string for new function code, got {type(new_functions_code)}")
            
            # 使用调整过缩进的代码进行解析
            new_functions_code = adjust_code_indentation(new_functions_code)
            new_functions_nodes = ast.parse(new_functions_code).body
            
            for new_node in new_functions_nodes:
                if isinstance(new_node, ast.FunctionDef) and new_node.name == function_name:
                    return new_node
        return node

def adjust_code_format(code):
    if isinstance(code, list):
        return "\n".join(code)  # 假设列表中每个元素都是一行代码
    elif isinstance(code, str):
        return code
    else:
        raise ValueError(f"Unsupported code format: {type(code)}")

# Main function to process the repository
def process_repository(to_implement_funcs, path_prefix, dest_path):
    
    logger_success("代码核对成功，进行替换")

    # Create a new directory for code replacement
    copy_project_structure(path_prefix, dest_path)

    # Build a dictionary for replacements
    replacements = {func['function']: adjust_code_format(func['code']) for func in to_implement_funcs}

    for func in to_implement_funcs:
        relative_file_path = func['file']
        file_path = os.path.join(dest_path, relative_file_path.replace("\\", os.sep))
        source_code = read_code(file_path)
        # Parse the source code into an AST
        tree = ast.parse(source_code)
        # Replace functions in the AST
        replacer = FunctionReplacer(replacements)
        modified_tree = replacer.visit(tree)
        # Convert the modified AST back to source code
        modified_code = astunparse.unparse(modified_tree)
        # Write the modified code back to the file
        write_code(file_path, modified_code)


class FunctionInfoVisitor(ast.NodeVisitor):
    def __init__(self):
        self.functions = []
        self.source_code = ""

    def visit_FunctionDef(self, node):
        # 收集函数定义的信息
        function_info = {
            'name': node.name,
            'code': self.source_code[node.lineno - 1:node.end_lineno],
            'signature': ast.unparse(node.args),
            'docstring': ast.get_docstring(node),
            'start_lineno': node.lineno,
            'end_lineno': node.end_lineno,
            'class': None  # 会在visit_ClassDef中处理
        }
        self.functions.append(function_info)
        self.generic_visit(node)

    def visit_ClassDef(self, node):
        # 处理类定义中的函数
        class_name = node.name
        for item in node.body:
            if isinstance(item, ast.FunctionDef):
                function_info = {
                    'name': item.name,
                    'code': self.source_code[item.lineno - 1:item.end_lineno],
                    'signature': ast.unparse(item.args),
                    'docstring': ast.get_docstring(item),
                    'start_lineno': item.lineno,
                    'end_lineno': item.end_lineno,
                    'class': class_name
                }
                self.functions.append(function_info)
        self.generic_visit(node)

def extract_function_info_from_string(source_code):
    corrected_code = adjust_code_indentation(source_code)
    tree = ast.parse(corrected_code)

    function_info_visitor = FunctionInfoVisitor()
    function_info_visitor.source_code = source_code.split('\n')  # 将源代码字符串按行分割
    function_info_visitor.visit(tree)

    return function_info_visitor.functions


def clean_path(old_path):
    # 正则表达式匹配 "E:\\...\\repoN\\" 这样的模式，其中 N 是一个或多个数字
    # 适应不同根目录和repo名，确保正则匹配到 'repo' 后的数字部分
    new_path = re.sub(r'.*\\repo\d+\\', '', old_path)
    return new_path
def unify_path_format(path):
    return path.replace('/', '\\')

class Task:
    def __init__(self, task_name, task_description, task_type, task_status, task_priority, task_deadline, task_assignee, task_creator):
        self.task_name = task_name
        self.task_description = task_description
        self.task_type = task_type
        self.task_status = task_status
        self.task_priority = task_priority
        self.task_deadline = task_deadline
        self.task_assignee = task_assignee
        self.task_creator = task_creator

    def get_task(self):
        readme = self.task_description
        task_type = self.task_type
        task_status = self.task_status
        task_priority = self.task_priority
        task_deadline = self.task_deadline
        task_assignee = self.task_assignee
        task_creator = self.task_creator

    #获取一个代码仓库的基本信息
    #有序组织进行输入
    #首先获得repoTask
    #随后对单独的repo进行操作
class repoManager:
    def __init__(self, 
                 repo_path=None,  
                 dataset_path=None,  
                 project_hierarchy=None,  
                 readme=None,  
                 repo_structure=None,  
                 repo_structure_dependency=None,  
                 code_detail=None,  
                 task=None,  
                 task_table=None):  
        self.repo_path = repo_path
        self.dataset_path = dataset_path
        self.readme = readme
        self.project_hierarchy = project_hierarchy
        self.repo_structure = repo_structure
        self.repo_structure_dependency = repo_structure_dependency
        self.code_detail = code_detail
        self.task = task
        self.task_table = task_table

    def get_raw_repo(self, ):
        if self.dataset_path:  # 检查是否设置了dataset_path
            repo_list = FileUtil.read_from_json(self.dataset_path)
            return repo_list
        else:
            print("No dataset path provided")

    def _readme(self):
        self.readme = {}
        repo_list = self.get_raw_repo()
        for repo in repo_list:
            self.readme[repo["repo_name"]] = repo["readme"]

    def _codesturcture(self):
        self.code_detail = {}
        repo_list = self.get_raw_repo()
        for repo in repo_list:
            self.code_detail[repo["repo_name"]] = repo["code_detail"]

        
    def _codeTask(self):
        self.task_table = {}
        repo_list = self.get_raw_repo()
        for repo in repo_list:
            for key, value in repo["task_table"].items():
                value["Path"] = unify_path_format(value['Path'])
            self.task_table[repo["repo_name"]] = repo["task_table"]

    # dict_function_base['start_lineno'].append(start_lineno)
    # dict_function_base['end_lineno'].append(end_lineno)
    # dict_function_base['repo name'].append(repo_name)
    # dict_function_base['file_path'].append(py_file)
    # dict_function_base['relative_file_path'].append(relative_file_path)
    # dict_function_base['fully_qualified_name'].append(fully_qualified_name)
    # dict_function_base['function_name'].append(function_name)
    # dict_function_base['raw_source_code'].append(raw_source_code)
    # dict_function_base['class'].append(class_name)
    # # dict_function_base['summary'].append(summary)
    # dict_function_base['comment_free_source_code'].append(comment_free_source_code)
    # dict_function_base['function signature'].append(function_signature)
    # dict_function_base['comment'].append(comment)
    # dict_function_base['local variables'].append(variables)
    # dict_function_base['is_empty_function'].append(is_empty)
    def get_raw_code(self,):
        self._codesturcture()
        self._codeTask()
        dict_raw_code = {}
        #给出的file_path和relative_file_path都是windows的全局路径
        for repo, content in self.code_detail.items():
            path_dict = content['file_path']
            fqn_list = content["fully_qualified_name"]
            function_name_list = content["function_name"] 
            signature_list = content["function signature"] #我觉得必要
            raw_source_code = content["raw_source_code"]
            comment_free_code = content["comment_free_source_code"]
            class_list = content["class"] #我觉得必要
            comment_list = content["comment"] #后续可再加
            local_variables_list = content["local variables"] #相关的变量
            third_party_libraries = content["third_party_libraries"] #我觉得必要
            is_empty_function = content["is_empty_function"]
            startlineno = content["start_lineno"]
            endlineno = content["end_lineno"]

           # 将函数签名、类名、局部变量整合到一个结构化字典中
            functions_v0_list = []
            functions_v1_list = []
            functions_details = []
            for index, signature in enumerate(signature_list):
                class_name = class_list[index] if index < len(class_list) else None
                local_variables = local_variables_list[index] if index < len(local_variables_list) else {}
                function_detail = {
                    "path" : clean_path(path_dict[index]),
                    "fqn_list" : fqn_list[index],
                    "class": class_name,
                    "signature": signature,
                    "comment" : comment_list[index],
                    "comment_free_code" : comment_free_code[index],
                    "start_lineno": startlineno[index],
                    "end_lineno": endlineno[index],
                    "comment" : comment_list[index],
                    "local_variables": local_variables,
                    "third_party_libraries": third_party_libraries,
                }
                functions_v0 = {
                    # "name" : function_name_list[index],
                    "path" : clean_path(path_dict[index]),
                    "fqn" : fqn_list[index],
                    "class": class_name,
                    "signature": signature,
                }
                #function_v1 - {path, fqn, class, signature, comment}
                functions_v1 = {
                    # "name" : function_name_list[index],
                    "path" : clean_path(path_dict[index]),
                    "fqn" : fqn_list[index],
                    "class": class_name,
                    "signature": signature,
                    "comment" : comment_list[index],
                    }
                functions_v0_list.append(functions_v0)
                functions_v1_list.append(functions_v1)
                functions_details.append(function_detail)

            code_structure = {
                "functions_detail": functions_details,
                "function_v0": functions_v0_list,
                "function_v1": functions_v1_list,
                "local_variables": local_variables_list,
                "third_party_libraries": third_party_libraries,
            }

            # 将结构化字典转换成JSON格式
            formatted_json = json.dumps(code_structure, indent=4, ensure_ascii=False)
            # print(formatted_json)
            # for key, value in self.task_table["repo1"].items():
            #     value["Path"] = unify_path_format(value['Path'])
            # print(self.task_table["repo1"])
            dict_raw_code[repo] = code_structure
        return dict_raw_code


    # 这里对应的是处理先前存储的数据集，尝试合并信息
    def preprocess_data(raw_data):
        processed_data = []
        
        # 创建一个字典来存储相同类和相同路径前缀的方法信息
        class_method_dict = {}
        
        for item in raw_data:
            path = item["path"]
            class_name = item.get("class")
            
            if class_name:
                class_method_dict.setdefault((path, class_name), []).append(item)
            else:
                # 对于没有类名的情况，直接添加到processed_data中
                processed_data.append({
                    "path_prefix": path,
                    "class": None,
                    "methods": [{
                        "fqn": item["fqn"],
                        "signature": item["signature"],
                        "comment": item["comment"]
                    }]
                })
        
        # 将相同类和相同路径前缀的方法信息合并到processed_data中
        for key, methods in class_method_dict.items():
            path_prefix, class_name = key
            processed_data.append({
                "path_prefix": path_prefix,
                "class": class_name,
                "methods": [{
                    "fqn": method["fqn"],
                    "signature": method["signature"],
                    "comment": method["comment"]
                } for method in methods]
            })
        
        return processed_data

    def get_code_framework():
        pass        


## 用来将数据转化成plan输入的格式
from collections import defaultdict
def transform_data(data):
    # Structure to hold the transformed data

    # # Given data (shortened for brevity)
    # data = [
    #     {'path': 'textual-universal-directorytree\\textual_universal_directorytree\\alternate_paths.py', 'fqn': 'textual-universal-directorytree.textual_universal_directorytree.alternate_paths._GitHubAccessor.__init__', 'class': 'textual-universal-directorytree.textual_universal_directorytree.alternate_paths._GitHubAccessor', 'signature': 'def __init__(self):', 'comment': 'Initialize the GitHub Accessor'},
    #     # Additional entries would follow in actual data...
    # ]

    # Structure to hold the transformed data
    transformed_data = defaultdict(lambda: {"path_prefix": None, "class": None, "methods": []})

    # Process each entry in the data
    for entry in data:
        key = (entry['path'], entry['class'])
        if transformed_data[key]["path_prefix"] is None:
            transformed_data[key]["path_prefix"] = entry['path']
            transformed_data[key]["class"] = entry['class']
        transformed_data[key]["methods"].append({
            "fqn": entry['fqn'],
            "signature": entry['signature'],
            "comment": entry['comment']
        })

    
    # Convert defaultdict to list as expected
    transformed_list = [value for key, value in transformed_data.items()]

    #进行部分合并
    consolidated = {}
    for item in transformed_list:
        # Use path and class as a unique key
        key = (item["path_prefix"], item["class"])
        if key not in consolidated:
            consolidated[key] = item
        else:
            # Append methods to existing class
            consolidated[key]["methods"].extend(item["methods"])

    # Extract values to get back to the list format
    consolidated_data = list(consolidated.values())

    return consolidated_data

# 生成代码规划任务
def generate_and_save_responses(api_inputs, filenames, plan_directory, repo_name, model_name, project_plan):
    repo_path = os.path.join(plan_directory, repo_name)
    if not os.path.exists(repo_path):
        os.makedirs(repo_path)
        logger.info(f"Created directory: {repo_path}")

    for api_input, filename in zip(api_inputs, filenames):
        logger.info("正在生成代码规划任务")
        messages = [{"role": "user", "content": project_plan}]
        
        try:
            token_count = LLMUtil.calculate_token_nums_for_prompt(project_plan)
            logger.info(f"Token count for prompt: {token_count}")
            if model_name == LLMUtil.GPT3_5_TURBO_MODEL_NAME:
                plan_json = LLMUtil.ask_gpt3_5turbo(messages, temperature=0.3)
            if model_name == LLMUtil.GPT4_0125_PREVIEW_MODEL_NAME:
                plan_json = LLMUtil.ask_gpt_4_preview(messages, temperature=0.3)
            if model_name == LLMUtil.GPT4_MODEL_NAME:
                plan_json = LLMUtil.ask_gpt_4_turbo(messages, temperature=0.3)
            if model_name == LLMUtil.GPT3_5_TURBO_16K_MODEL_NAME:
                plan_json = LLMUtil.ask_gpt3_5turbo16k(messages, temperature=0.3)
            
            json_data = json.loads(plan_json)
            # print(json_data["development_plan"])
            filepath = os.path.join(repo_path, filename)
            with open(filepath, 'w') as json_file:
                json.dump(json_data, json_file, indent=2)
                logger.success(f"Saved API response to {filepath}")
        
        except Exception as e:
            logger.error(f"Failed to generate or save plan for {api_input}. Error: {e}")


def generate_api_inputs_and_filenames(number_of_calls, gpt_model):
    api_inputs = [f"input{i}" for i in range(1, number_of_calls + 1)]
    filenames = [f"response{i}_{gpt_model}.json" for i in range(1, number_of_calls + 1)]
    return api_inputs, filenames


def enhance_task_with_code_info(development_plan, fd):
    """
    Enhance tasks in the development plan with additional code information.
    :param development_plan: List of steps in the development plan, where each step contains tasks.
    :param fd: List of function details extracted from the source code.
    """
    for step in development_plan:
        for task in step['tasks']:
            task["comment"] = []
            task["local_variables"] = []
            task["third_party_libraries"] = []
            for method in task["functions"]:
                for item in fd:
                    if item["fqn_list"].endswith(method) and item["path"].endswith(task["module"]):
                        task["comment"].append(item["comment"])
                        task["local_variables"].append(item["local_variables"])
                        task["third_party_libraries"].append(item["third_party_libraries"])
    return development_plan





def get_refer_context(step, development_plan):
    refer_list = []
    refer_list_index = step['reference']                
    if refer_list_index is not None:
        logger.info("加入规划中的refernce内部依赖")
        for step1 in development_plan:
            if step1['step'] in refer_list_index:
                logger.info("成功")
                refer_list.append(step1)
    else:
        refer_list = None
    return refer_list





def get_combined_generation_code(messages, combined_generation_code, max_attempts=5):
    attempt = 0
    while attempt < max_attempts:
        try:
            development_json = select_model(selected_model, messages)
            # development_json = LLMUtil.ask_gpt3_5turbo(messages, temperature=0.3)
            logger.info(LLMUtil.calculate_token_nums_for_prompt(development_json))
            # logger.info(development_json)
            json_data = json.loads(development_json)
            combined_generation_code["implementation_plan"].append(json_data["implementation_plan"])
            combined_generation_code["Third-party_libraries"].append(json_data["third_party_libraries"])
            return combined_generation_code
        except json.JSONDecodeError as e:
            logger.error(f"JSON decoding failed on attempt {attempt + 1}: {str(e)}")
            attempt += 1
    logger.error("Failed to process the message after several attempts.")
    raise Exception("Failed to process the message after several attempts.")


def get_refactor_code(messages, method_name, max_attempts=5):
    attempt = 0
    while attempt < max_attempts:
        try:
            development_json = select_model(selected_model, messages)
            # development_json = LLMUtil.ask_gpt3_5turbo(messages, temperature=0.3)
            logger.info(LLMUtil.calculate_token_nums_for_prompt(development_json))
            # logger.info(development_json)
            json_data = json.loads(development_json)
            new_code = json_data["code"]
            verify_pass_method, code = check_code_quality(new_code, task)
            if method_name not in verify_pass_method["functions_with_pass"]:
                return code
        except json.JSONDecodeError as e:
            logger.error(f"JSON decoding failed on attempt {attempt + 1}: {str(e)}")
            attempt += 1
    logger.error("Failed to generate code without pass after several attempts.")
    return "error"

def check_method_keyword(task):
    method = task["method"]
    if "method" in task:
        method = task["method"]
    elif "methods" in task:
        logger.error("function关键词已经被废弃, 请使用method关键词")
        method = task["methods"]
    elif "function" in task:
        logger.error("function关键词已经被废弃, 请使用method关键词")
        method = task["function"]
    elif "functions" in task:
        logger.error("function关键词已经被废弃, 请使用method关键词")
        method = task["functions"]
    else:
        raise ValueError("未找到method关键词")
    return method

    
def verify_method_coverage(implementation_plan, method_all_todo, development_plan):
    # 创建字典来跟踪已经找到的方法及其代码
    covered_methods = {}
    to_implement_funcs = []
    # 遍历实施计划中的所有步骤和任务
    for index, step in enumerate(implementation_plan):
        step = step[0]
        for task in step["tasks"]:
            file_path = task["file"]
            if "implementation_details" not in task:
                print(f"任务 {task} 没有实施细节")
            code = task["implementation_details"]["Code"]
            class_belong = task["class"]
            verify_pass_method, code = check_code_quality(code, task)
            functions_info = extract_function_info_from_string(code)
            for info in functions_info:
                dict_res = {"module": file_path, "class": class_belong, "function": info["name"]}
                method_key = frozenset(dict_res.items())  # 现在仅基于三个关键信息生成 key
                for m in method_all_todo:
                    method_todo_key = frozenset({("module", m["module"]), ("class", m["class"]), ("function", m["function"])})
                    if method_key == method_todo_key:
                # if method_key in {frozenset({("module", m["module"]), ("class", m["class"]), ("function", m["function"])}.items()) for m in method_all_todo}:
                        if method_key in covered_methods:
                            # 检查新旧代码片段长度，并决定是否更新已存的代码片段
                            if len(info["code"]) > len(covered_methods[method_key]):
                                covered_methods[method_key] = info["code"]
                        else:
                            covered_methods[method_key] = info["code"]
                        m["coverage"] = True
                        m["code"] = info["code"]
                        m["step"] = step["step"]
                        if info["name"] in verify_pass_method["functions_with_pass"]:
                            m["pass_factor"] = True
    
    # 根据三个基本关键词检查覆盖情况
    method_all_todo_set = {frozenset({("module", m["module"]), ("class", m["class"]), ("function", m["function"])}) for m in method_all_todo}
    covered_method_keys = set(covered_methods.keys())
    if not covered_method_keys >= method_all_todo_set:
        uncovered_methods = method_all_todo_set - covered_method_keys
        print("以下方法未被覆盖:")
        for method in uncovered_methods:
            print({k: v for k, v in method})
    


    to_implement_funcs = [m for m in method_all_todo if m["coverage"] == True and m["function"] != "__init__"]
    to_implement_funcs_with_pass = [m for m in to_implement_funcs if m["pass_factor"] == True]
    logger.info(f"共覆盖函数{len(to_implement_funcs)}个")
    logger.info(f"共有函数{len(method_all_todo_set)}个")
    logger.info(f"覆盖函数{len(to_implement_funcs_with_pass)}个函数中的pass未被覆盖")

    logger.info("----------------------------------------------")
    logger.info(f"对pass函数进行重新生成")

    for i in tqdm(to_implement_funcs, desc="正在重构pass函数", ):
        if i["pass_factor"] == True:
            step = i["step"]
            logger.info(f"任务{step}中的函数{i['function']}的pass未被覆盖")
            context_code = []
            for step in development_plan:
                if step['step'] == i["step"]:
                    # get generated_context code
                    for task in step['tasks']:
                        module = task['module']
                        class_name = task['class']
                        functions = task['functions']
                        for func in functions:
                            dict_res = {
                                "module": module,
                                "class": class_name,
                                "functions": func
                            }
                            for m in method_all_todo:
                                method_todo_key = frozenset(
                                    {("module", m["module"]), ("class", m["class"]), ("function", m["function"])})
                                if dict_res == method_todo_key:
                                    context_code.append(m["code"])
            logger.info("-------------------------------")
            refer_list = get_refer_context(step, development_plan)
            psip = project_step_implementation_generation_pass
            logger.info("对每个规划任务中batchsize个函数生成代码实现")
            task_with_pass_function = {
                'module': i['module'],
                'class': i['class'],
                'functions': [i]
            }
            step["tasks"] = [task_with_pass_function]
            psip = psip.format(project_readme=repomanager.readme[repo_name], code_framework=step, reference = refer_list, generated_context=context_code, comment=i["comment"], local_variables=i["local_variables"], third_party_libraries=i["third_party_libraries"])
            # logger.info(step)
            messages = [{"role": "user", "content": psip}]
            code = get_refactor_code(messages, i["function"])
            if code == "error":
                logger.error(f"Failed to refactor code for function {i['function']} in task {step}")
            else:
                i["code"] = code
                i["pass_factor"] = False
                logger.info(f"Successfully refactored code for function {i['function']} in task {step}")
    to_implement_funcs_with_pass = [m for m in to_implement_funcs if m["pass_factor"] == True]
    logger.info(f"覆盖函数{len(to_implement_funcs_with_pass)}个函数中的pass未被覆盖")
    return to_implement_funcs


#主要用于处理输出的json response是否符合规范
# 目前使用gpt3.5turbo进行生成
def validate_json_format(data):
    
    return True  # For demonstration purposes

def validate_and_process_responses(filenames, repo_path):
    valid_data = None
    for filename in filenames:
        filepath = os.path.join(repo_path, filename)
        try:
            with open(filepath, 'r') as json_file:
                data_str = json_file.read()  # 读取的内容是一个字符串
                data = json.loads(data_str)  # 将字符串反序列化为JSON对象
                if validate_json_format(data):
                    valid_data = data
                    logger.info(f"Successfully read and validated: {filename}")
                    break
        except Exception as e:
            logger.error(f"Error reading or validating {filename}: {e}")
    
    if valid_data is not None:
        logger.info("Proceeding with the valid data")
        # 这里添加处理valid_data的逻辑
        logger.info("代码规划任务完成, 接下来进行分任务生成")
    else:
        logger.warning("No valid JSON files were found.")
    
    return valid_data


def insert_imports(file_path, imports):
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    # Find the position to insert imports (after the last existing import)
    import_position = 0
    for i, line in enumerate(lines):
        if line.strip().startswith('import') or line.strip().startswith('from'):
            import_position = i + 1

    # Insert new imports if they are not already present
    for new_import in sorted(imports):
        if new_import + '\n' not in lines:
            lines.insert(import_position, new_import + '\n')
            import_position += 1

    # Write back the modified lines to the file
    with open(file_path, 'w', encoding='utf-8') as file:
        file.writelines(lines)

def extract_import_statements(third_party_libraries):
    import_statements = set()
    for library in third_party_libraries:
        import_statement = f"import {library}"
        import_statements.add(import_statement)
    return import_statements


def update_source_files_with_imports(implementation_plan):
    # 此处third_party_libraries是一个列表，包含了所有的第三方库，只为了后续方便进行本地环境的第三方库pip做铺垫
    third_party_libraries = []
    for func in implementation_plan:
        relative_file_path = func['file']
        imports = extract_import_statements(func['third_party_libraries'])
        for library in func['third_party_libraries']:
            third_party_libraries.append(library)
        file_path = os.path.join(dest_path, relative_file_path.replace("\\", os.sep))
        if file_path and os.path.exists(file_path):
            # Insert the import statements into the source file
            insert_imports(file_path, imports)
    return third_party_libraries

import subprocess

# def run_command(command, cwd=None):
#     """Run a system command and capture the output."""
#     result = subprocess.run(command, cwd=cwd, shell=True, check=True, text=True, capture_output=True)
#     return result.stdout
def run_command(command, cwd=None, env=None):
    """Run a system command and capture the output."""
    full_command = command
    if env:
        full_command = f"conda run -n {env} {command}"
    try:
        result = subprocess.run(
            full_command,
            cwd=cwd,
            shell=True,
            check=True,
            text=True,
            capture_output=True,
            encoding='utf-8',
            errors='replace'  # This will replace errors with a replacement character
        )
        return result.stdout
    except subprocess.CalledProcessError as e:
        print(f"Error executing command: {full_command}")
        print(f"Return code: {e.returncode}")
        print(f"Output: {e.stdout}")
        print(f"Error: {e.stderr}")
        # raise



def parse_pytest_output(output):
    """Parse the output of pytest to extract test results."""
    results = {
        'passed': 0,
        'failed': 0,
        'skipped': 0,
        'errors': 0,
    }
    match = re.search(r'(\d+) passed', output)
    if match:
        results['passed'] = int(match.group(1))
    match = re.search(r'(\d+) failed', output)
    if match:
        results['failed'] = int(match.group(1))
    match = re.search(r'(\d+) skipped', output)
    if match:
        results['skipped'] = int(match.group(1))
    match = re.search(r'(\d+) errors?', output)
    if match:
        results['errors'] = int(match.group(1))
    return results


def parse_django_output(output):
    """Parse the output of django-admin test to extract test results."""
    results = {
        'total': 0,
        'passed': 0,
        'failed': 0,
        'errors': 0,
        'skipped': 0,
    }
    
    # Check for the number of tests run
    match = re.search(r'Ran (\d+) test', output)
    if match:
        results['total'] = int(match.group(1))

    # Check for individual test case results
    results['passed'] = len(re.findall(r'... ok', output))
    results['failed'] = len(re.findall(r'... FAIL', output))
    results['errors'] = len(re.findall(r'... ERROR', output))
    results['skipped'] = len(re.findall(r'... skipped', output))
    
    # If there are no failed or error results, assume all tests passed
    if 'OK' in output:
        results['passed'] = results['total']

    return results

def run_tests(repo_name, env_dict):
    env = env_dict["env"]
    path = env_dict["path"]
    commands = env_dict["commands"]
    if env:
        run_command(f"conda activate {env}")
    # Change to the repository directory
    os.chdir(path)
    # Run each command in the list of commands
    repo_results = []
    for command in commands:
        output = run_command(command, cwd=path, env=env)
        if 'pytest' in command:
            results = parse_pytest_output(output)
            repo_results.append(results)
            print(f"Results for {repo_name}:\n{results}\n")
        elif 'django-admin test' in command or 'coverage' in command:
            results = parse_django_output(output)
            repo_results.append(results)
            print(f"Results for {repo_name} (django-admin test or coverage):\n{results}\n")
    if repo_results:
        return repo_results[0]
    else:
        print(f"No test results found for {repo_name}")
        return None



# def run_tests(repo_name, env_dict):
#     env = env_dict["env"]
#     path = env_dict["path"]
#     commands = env_dict["commands"]
#     if env:
#         run_command(f"conda activate {env}")
#     os.chdir(path)
#     # Run each command in the list of commands
#     repo_results = []
#     for command in commands:
#         output = run_command(command)
#         if 'pytest' in command:
#             results = parse_pytest_output(output)
#             repo_results.append(results)
#             print(f"Results for {repo_name}:\n{results}\n")
#         elif 'django-admin test' in command or 'coverage' in command:
#             results = parse_django_output(output)
#             repo_results.append(results)
#             print(f"Results for {repo_name} (django-admin test or coverage):\n{results}\n")

#     # Deactivate the Conda environment
#     if env:
#         run_command("conda deactivate")
#     if repo_results != []:
#         return repo_results[0]
#     else:
#         logger.error(f"No test results found for {repo_name}")

## 需不需要变成类似于fixed repo agent
# def check_code_quality(code, task):
#     # 试图自动调整代码块的缩进
#     code = textwrap.dedent(code).strip()
#     try:
#         tree = ast.parse(code)
#         results = {
#                 "functions_with_pass": []}
#         for node in ast.walk(tree):
#             if isinstance(node, ast.FunctionDef):
#                 pass_refactor = False
#                 for sub_node in node.body:
#                     if isinstance(sub_node, (ast.Pass)):
#                         pass_refactor = True
#                         break
#                 if pass_refactor:
#                     results["functions_with_pass"].append(node.name)
#         return results

#     except SyntaxError as e:
#         messages = [{"role": "user", "content": fixed_prompt.format(code_to_be_implemented=code, error_description=str(e), method_information=task)}]
#         verify_json = LLMUtil.ask_gpt3_5turbo(messages, temperature=0)
#         json_data = json.loads(verify_json)
#         new_code = json_data["code"]
#         return {"error": f"Syntax error in code: {str(e)}", "Code": new_code}

def check_code_quality(code, task):
    # 尝试自动调整代码块的缩进
    code = textwrap.dedent(code).strip()
    max_attempts = 10
    attempt_tree = 0
    attempt_json = 0

    while attempt_tree < max_attempts and attempt_json < max_attempts:
        try:
            tree = ast.parse(code)
            results = {
                    "functions_with_pass": []}
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    pass_refactor = False
                    for sub_node in node.body:
                        if isinstance(sub_node, (ast.Pass)):
                            pass_refactor = True
                            break
                    if pass_refactor:
                        results["functions_with_pass"].append(node.name)
            return results, code
        except SyntaxError as e:
            attempt_tree += 1
            # 格式化提示信息并请求修复代码
            messages = [{
                "role": "user",
                "content": fixed_prompt.format(code_to_be_implemented=code, error_description=str(e), method_information=task)
            }]
        try:
            verify_json = select_model(selected_model, messages, temperature=0)
            # verify_json = LLMUtil.ask_gpt3_5turbo(messages, temperature=0)
            json_data = json.loads(verify_json)
            new_code = json_data.get("code")
            code = new_code  # 更新代码尝试再次编译
        except json.JSONDecodeError as e:
            logger.error(f"JSON decoding failed on attempt {attempt_tree + 1}: {str(e)}")
            attempt_json += 1


    # 如果所有尝试都失败，返回错误信息
    raise ValueError(f"Syntax error in code after {max_attempts}")



#----------------------------------------implementation----------------------------------------------

from prompt import system_prompt1,system_prompt2, user_prompt2, system_prompt3, user_prompt3
from dataset.preprocess import FunctionBaseConstruction, extract_files_and_save
from prompt2 import user_prompt2_1, user_prompt2_2, user_prompt2_3, user_prompt2_4, user_prompt2_3_1, user_prompt2_3_2, project_plan_generation, project_step_implementation_generation, fixed_prompt, project_step_implementation_generation_pass
from log import logger

repo_path = r"E:\academic\projectGeneration\python_project\repo copy 4"
dest_path = r"E:\academic\reuseProject\project_generation\repo_result"
dataset_path = r"E:\academic\reuseProject\project_generation\dataset\python_copy\dataset_add_doc_readme_codeStructure_callHierachy.json"
plan_directory = r"E:\academic\reuseProject\project_generation\plan"

list_repo_savad = [ "repo11"]
## "repo1" and "repo7" "repo3", "repo4(莫名其妙空出来一行，不知道在干嘛)",   "repo5"(不生method关键词，结果用的function),"repo6"(替换的时候又寄了)， "repo8", repo10 assert数量出错。啊？？ 
repositories = {
    "repo1": {
        "env": "hatch_env",
        "path": os.path.join(dest_path, "repo1", "textual-universal-directorytree"),
        "commands": [
            "pytest ."
        ]
    },
    "repo3": {
        "env": "django_tem",
        "path": os.path.join(dest_path, "repo3", "django-template-partials"),
        "commands": [
            "django-admin test --settings=tests.settings --pythonpath=. --verbosity=3"
        ]
    },
    "repo4": {
        "env": "ufomerge",
        "path": os.path.join(dest_path, "repo4", "ufomerge"),
        "commands": [
            "pytest ."
        ]
    },
    "repo5": {
        "env": "att721",
        "path": os.path.join(dest_path, "repo5", "activation_tracker"),
        "commands": [
            "pytest ."
        ]
    },
    "repo6": {
        "env": "att721",
        "path": os.path.join(dest_path, "repo6", "constrainedlr"),
        "commands": [
            "pytest ."
        ]
    },
    "repo8": {
        "env": "translategram",
        "path": os.path.join(dest_path, "repo8", "translategram"),
        "commands": [
            "pytest ."
        ]
    },
    "repo10": {
        "env": "fastapi",
        "path": os.path.join(dest_path, "repo10", "fastapi-dapr-helper"),
        "commands": [
            "pytest ."
        ]
    },
    "repo11": {
        "env": "att721",
        "path": os.path.join(dest_path, "repo11", "boggle"),
        "commands": [
            "pytest ."
        ]
    }
}


all_eval_results = {}
fbc = FunctionBaseConstruction()
code_structure_try = False
#plan_num 是设定生成多少个answer
plan_num = 3
#控制本次调用是否生成代码
code_gen = False
valid_gen = False
replace_gen = False
library_gen = True
test_gen = False
#为True进行，单个函数生成，不为True进行总体生成
function_pattern = True
function_batch_size = 3
# if model_name == LLMUtil.GPT3_5_TURBO_MODEL_NAME:
#     plan_json = LLMUtil.ask_gpt3_5turbo(messages, temperature=0.3)
# if model_name == LLMUtil.GPT4_0125_PREVIEW_MODEL_NAME:
#     plan_json = LLMUtil.ask_gpt_4_preview(messages, temperature=0.3)
# if model_name == LLMUtil.GPT4_MODEL_NAME:
#     plan_json = LLMUtil.ask_gpt_4_turbo(messages, temperature=0.3)
# if model_name == LLMUtil.GPT3_5_TURBO_16K_MODEL_NAME:
#     plan_json = LLMUtil.ask_gpt3_5turbo16k(messages, temperature=0.3)

# selected_model = LLMUtil.GPT3_5_TURBO_MODEL_NAME
# selected_model = LLMUtil.GPT3_5_TURBO_16K_MODEL_NAME
# selected_model = LLMUtil.GPT4_MODEL_NAME
# selected_model = LLMUtil.GPT4_0125_PREVIEW_MODEL_NAME

selected_model = LLMUtil.GPT3_5_TURBO_MODEL_NAME

if os.path.exists(plan_directory) == False:
    os.makedirs(plan_directory)



if __name__ == "__main__":
    repomanager = repoManager(dataset_path=dataset_path)
    # repomanager.get_readme()
    # for i in list_repo_savad:
    #     print("----------------------------------------------------")
    #     print(repomanager.readme[i])
    repomanager.get_raw_code()
    # repomanager.get_code_description()
    repomanager._readme()
    dict_raw_code = repomanager.get_raw_code()

    for repo_name in list_repo_savad:
        #1. 读取存储数据集中初始的信息 （仓储库元信息）
        code_structure = dict_raw_code[repo_name]
        fd = code_structure["functions_detail"]

        cgc_path = os.path.join(plan_directory, repo_name, f"{repo_name}_combined_generation_code.json")

        # print(fd)

        # 3 生成代码规划任务
        logger.info("生成代码规划任务")
        logger.info("----------------------------------------------------")
        #3.1 代码规划任务
        #别忘了把先前的信息输入进去
         
        #这一部分可能对后面有用，但我还没想好怎么做
        logger.trace("reference: ")
        logger.trace("----------------------------------------------------")
        logger.trace(repomanager.task_table[repo_name])
        # print(repomanager.task_table[repo_name])
    
        #3.2 具体任务输出
        logger.info(f"落实{repo_name}规划任务输出")
        logger.info("----------------------------------------------------")
        
        plg = project_plan_generation
        plg = plg.format(code_framework=transform_data(code_structure["function_v1"]))
        # print(code_structure["function_v1"])
        

#-----------------------------------------------------------生成核心区---------------------------------------------------
        # 这里我们将生成3个diamagnetic任务进行备份 
        # 生成3个API调用的输入和文件名
        api_inputs, filenames = generate_api_inputs_and_filenames(plan_num, selected_model)

        # 生成并保存API响应
        # generate_and_save_responses(api_inputs, filenames, plan_directory, repo_name, selected_model, plg)
        logger.info("--------------------------------------------------")
        logger.info("规划结果核验")
        # 选择其中没有报错的json文件
        # 核对其中没有报错的文件
        valid_data =  validate_and_process_responses(filenames, os.path.join(plan_directory, repo_name))
        
        
        method_all_todo = []
        for step in valid_data["development_plan"]:
            for task in step["tasks"]:
                if "commment" not in task:
                    task["comment"] = []
                if "local_variables" not in task:
                    task["local_variables"] = []
                if "third_party_libraries" not in task:
                    task["third_party_libraries"] = []
                for function in task["functions"]:
                    for item in fd:
                        # print(item["fqn_list"])
                        if item["fqn_list"].endswith(function) and item["path"].endswith(task["module"]):
                            task["comment"].append(item["comment"])
                            task["local_variables"].append(item["local_variables"])
                            task["third_party_libraries"].append(item["third_party_libraries"])
                            dict_res = {}
                            dict_res["module"] = task["module"]
                            dict_res["class"] = task["class"]
                            dict_res["function"] = function
                            # if dict_res not in method_all_todo:
                            #     method_all_todo.append(dict_res)
                            dict_res["comment"] = item["comment"]
                            dict_res["local_variables"] = item["local_variables"]
                            dict_res["third_party_libraries"] = item["third_party_libraries"]
                            dict_res["file"] = item["path"]
                            dict_res["pass_factor"] = False
                            dict_res["coverage"] = False
                            dict_res["start_lineno"] = item["start_lineno"]
                            dict_res["end_lineo"] = item["end_lineno"]
                            if dict_res not in method_all_todo:
                                method_all_todo.append(dict_res)

        

        development_plan = valid_data["development_plan"] 
        logger.info("-------------------------------------")
        logger.info("------------源代码信息补充---------")

        development_plan = enhance_task_with_code_info(development_plan, fd)
        logger.success("源代码信息补充完成")

        if code_gen == True:
            logger.info("开始分布任务生成")
            development_plan = valid_data["development_plan"] #其实就是读取了所有的信息
            # 遍历开发计划中的每个步骤
            # logger.info("-------------------------------------")
            # logger.info("------------源代码信息补充---------")

            # development_plan = enhance_task_with_code_info(development_plan, fd)
            # logger.success("源代码信息补充完成")
            logger.info("--------------------------------------")
            logger.info(f"{repo_name} -- 任务生成开始".format(repo_name=repo_name))

            combined_generation_code = {"implementation_plan": [],"Third-party_libraries": []}
            
            psi = project_step_implementation_generation

            for step in tqdm(development_plan, desc=f"{repo_name} -- 任务生成中"):
                refer_list = get_refer_context(step, development_plan)
                # 坏处同样比较明显，就是当一个plan可能被划分为了一个子任务，但这个子任务过大，所以需要进行再细致的划分。
                psi = project_step_implementation_generation
                if function_pattern is False:
                    logger.info("对每个规划任务直接生成代码实现")
                    psi = psi.format(project_readme=repomanager.readme[repo_name], code_framework=step,reference=refer_list,comment=task["comment"], local_variables=task["local_variables"], third_party_libraries=task["third_party_libraries"])
                    messages = [{"role": "user", "content": psi}]
                    combined_generation_code = get_combined_generation_code(messages, combined_generation_code)
                else:
                    logger.info("对每个规划任务中batchsize个函数生成代码实现")
                    batchsize = function_batch_size  # 你可以根据需要调整这个批处理大小
                    
                    for task in step['tasks']:
                        if function_batch_size < len(task['functions']):
                            function_batches = [task['functions'][i:i + batchsize] for i in range(0, len(task['functions']), batchsize)]
                            comment_batches = [task['comment'][i:i + batchsize] for i in range(0, len(task['comment']), batchsize)]
                            local_variables_batches = [task['local_variables'][i:i + batchsize] for i in range(0, len(task['local_variables']), batchsize)]
                            for batch in function_batches:
                                task_with_batch_functions = {
                                    'module': task['module'],
                                    'class': task['class'],
                                    'functions': batch
                                    }
                                psi = project_step_implementation_generation
                                step["tasks"] = [task_with_batch_functions]
                                psi = psi.format(project_readme=repomanager.readme[repo_name], code_framework=step, reference=refer_list, comment=comment_batches, local_variables=local_variables_batches, third_party_libraries=task["third_party_libraries"])
                                logger.info(step)
                                messages = [{"role": "user", "content": psi}]
                                combined_generation_code = get_combined_generation_code(messages, combined_generation_code)
                        else:
                                psi = psi.format(project_readme=repomanager.readme[repo_name], code_framework=step,reference=refer_list,comment=task["comment"], local_variables=task["local_variables"], third_party_libraries=task["third_party_libraries"])
                                messages = [{"role": "user", "content": psi}]
                                combined_generation_code = get_combined_generation_code(messages, combined_generation_code)
            

            logger.success(f"{repo_name}_代码实现生成成功")
            try:
                with open(cgc_path, "w", encoding="utf-8") as f:
                    json.dump(combined_generation_code, f, indent=4)
                    logger.success(f"Saved combined generation code to {cgc_path}")
            except Exception as e:
                logger.error(f"Failed to save combined generation code: {e}")
        with open(cgc_path, "r", encoding="utf-8") as f:
            combined_generation_code = json.load(f)
        if valid_gen == True:
            logger.info("---------进入测评阶段------------")
            logger.info("解析输出信息")
            # 接下啦解析并进行替换
            implementation_plan = combined_generation_code["implementation_plan"]
            third_party_libraries = combined_generation_code["Third-party_libraries"]
            # 这一步原理本身应该只需要的是File, method, implementation_plan和third_party_libraries
            to_implement_funcs = []
            function_num = 0
            function_num_ = len(method_all_todo)
            logger.info("代码初次生成成功，进行代码核对与重构")
            logger.info("----------------------------------------------------")
            # 进行代码方法覆盖核对，以及进行代码的格式化错误与存在pass的重构
            to_implement_funcs = verify_method_coverage(implementation_plan, method_all_todo, development_plan)
            save_data(to_implement_funcs, os.path.join(plan_directory, repo_name, f"{repo_name}_to_implement_funcs.pkl"))
        if replace_gen == True:
            logger.success("代码核对与重构成功, 进行替换")
            logger.info("----------------------------------------------------")
            to_implement_funcs = load_data(os.path.join(plan_directory, repo_name, f"{repo_name}_to_implement_funcs.pkl"))
            path_prefix = os.path.join(repo_path, repo_name)
            dest_path = os.path.join(dest_path, repo_name)
            print("---------*********************-----------------")
            logger.info("执行代码替换任务")
            process_repository(to_implement_funcs, path_prefix, dest_path)
            logger.success(f"{repo_name}_函数替换成功")
        if library_gen == True:
            to_implement_funcs = load_data(os.path.join(plan_directory, repo_name, f"{repo_name}_to_implement_funcs.pkl"))
            logger.info("----------------------------------------------------")
            logger.info("增添第三方库信息")
            libs =  update_source_files_with_imports(to_implement_funcs)
            logger.success(f"{repo_name}_第三方库信息增添成功")
        if test_gen == True:
            logger.info("----------------------------------------------------")
            # 进行环境的自动转换，自动化测试命令编写
            # 需要补全方法libs
            logger.info("环境自动转换")
            env_dict = repositories[repo_name]
            test_result = run_tests(repo_name, env_dict)
            all_eval_results[repo_name] = test_result
            logger.info("---------------------------------------------------")
            logger.info("{repo_name}测试完成")
            print(all_eval_results)
            logger.info("---------------------------------------------------")
            
        

            
        



































# for repo, content in self.code_detail.items():
#             path_dict = content['file_path']
#             reflect_base["fqn"] = content["fully_qualified_name"]
#             function_name_list = content["function_name"] 
#             signature_list = content["function signature"] #我觉得必要
#             raw_source_code = content["raw_source_code"]
#             comment_free_code = content["comment_free_source_code"]
#             class_list = content["class"] #我觉得必要
#             comment_list = content["comment"] #后续可再加
#             local_variables_list = content["local variables"] #相关的变量
#             third_party_libraries = content["third_party_libraries"] #我觉得必要
#             is_empty_function = content["is_empty_function"]


                # print(f"Step {step['step']}: {step['description']}")
                # print("Tasks:")
                # for task in step['tasks']:
                #     print(f"  Module: {task['module']}, Class: {task['class']}")
                #     print("  Functions:", ', '.join(task['functions']))
                # if step['reference_logic']:
                #     print("Reference Logic:", step['reference_logic'])
                # if step['reference']:
                #     print("References:", ', '.join(str(ref) for ref in step['reference']))


