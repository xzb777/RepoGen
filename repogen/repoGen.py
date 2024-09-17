import json
import re
from llm_util import LLMUtil
from tqdm import tqdm
import astunparse
import ast
from collections import defaultdict
import shutil
import os
import textwrap
import subprocess
import html
from merge_info import get_static_info
import sys
import io
from get_varaible import get_class_variables
from test_get import run_test
from test_get import handle_docker_setup, handle_docker_setup_before_copy
import argparse
from prompt import   fixed_prompt, project_step_implementation_generation_base, project_step_implementation_generation_base_with_init, project_plan_module_generation, project_plan_using_module_generation, project_plan_module_generation_claude, project_plan_using_module_generation_claude, project_step_implementation_generation_base_claude, project_step_implementation_generation_base_with_init_claude, fixed_prompt_claude, project_step_implementation_generation_base_design, project_step_implementation_generation_base_with_init_design
from loguru import logger

logger = logger.opt(colors=True)
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

def double_braces(input_string):
    input_string = re.sub(r'(?<!\{)\{(?!\{)', '{{', input_string)
    input_string = re.sub(r'(?<!\})\}(?!\})', '}}', input_string)
    return input_string

def copy_project_structure(src, dest):
    if os.path.exists(dest):
        shutil.rmtree(dest)
    shutil.copytree(src, dest)
def adjust_code_indentation(code):
    return textwrap.dedent(code).strip()
    
def adjust_code_format(code):
    if isinstance(code, list):
        return "\n".join(code) 
    elif isinstance(code, str):
        return code
    else:
        raise ValueError(f"Unsupported code format: {type(code)}")

def generate_and_save_responses(api_inputs, filenames, plan_directory, repo_name, model_name, project_plan, current_strategy):
    repo_path = os.path.join(plan_directory,current_strategy, model_name, repo_name)
    if not os.path.exists(repo_path):
        os.makedirs(repo_path)
        logger.info(f"Created directory: {repo_path}")
    for api_input, filename in zip(api_inputs, filenames):
        logger.info("Generating code planning tasks")
        messages = [{"role": "user", "content": project_plan}]
        try:
            token_count = LLMUtil.calculate_token_nums_for_prompt(project_plan)
            logger.info(f"Token count for prompt: {token_count}")
            if model_name == LLMUtil.GPT3_5_TURBO_MODEL_NAME:
                plan_json = LLMUtil.ask_gpt3_5turbo(messages, temperature=0.3)
            elif model_name == LLMUtil.GPT4_0125_PREVIEW_MODEL_NAME:
                plan_json = LLMUtil.ask_gpt_4_preview(messages, temperature=0.3)
            elif model_name == LLMUtil.GPT4_1106_PREVIEW_MODEL_NAME:
                plan_json =  LLMUtil.ask_gpt4_1106_turbo_preview(messages, temperature=0.3)
            elif model_name == LLMUtil.GPT4_TURBO_PREVIEW_MODEL_NAME:
                plan_json =  LLMUtil.ask_gpt4_turbo_preview(messages, temperature=0.3)
            elif model_name == LLMUtil.GPT4_MODEL_NAME:
                plan_json = LLMUtil.ask_gpt_4_turbo(messages, temperature=0.3)
            elif model_name == LLMUtil.GPT3_5_TURBO_16K_MODEL_NAME:
                plan_json = LLMUtil.ask_gpt3_5turbo16k(messages, temperature=0.3)
            elif model_name == LLMUtil.GPT3_5_TURBO_1106_MODEL_NAME:
                plan_json =  LLMUtil.ask_gpt35_1106_turbo_preview(messages, temperature=0.3)
            elif model_name == LLMUtil.GPT3_5_TURBO_0125_MODEL_NAME:
                plan_json =  LLMUtil.ask_gpt3_5turbo_json(messages,temperature=0.3)                
            # print(plan_json)
            json_data = json.loads(plan_json)
            filepath = os.path.join(repo_path, filename)
            with open(filepath, 'w') as json_file:
                json.dump(json_data, json_file, indent=2)
                logger.success(f"Saved API response to {filepath}")
        except Exception as e:
            logger.error(f"Failed to generate or save plan for {api_input}. Error: {e}")

def generate_and_save_responses_concise(filename, plan_directory, repo_name, model_name, project_plan, current_strategy):
    repo_path = os.path.join(plan_directory,current_strategy, model_name, repo_name)
    if not os.path.exists(repo_path):
        os.makedirs(repo_path)
        logger.info(f"Created directory: {repo_path}")
    logger.info("Generating code planning tasks")
    messages = [{"role": "user", "content": project_plan}]
    try:
        token_count = LLMUtil.calculate_token_nums_for_prompt(project_plan)
        logger.info(f"Token count for prompt: {token_count}")
        if model_name == LLMUtil.GPT3_5_TURBO_MODEL_NAME:
            plan_json = LLMUtil.ask_gpt3_5turbo(messages, temperature=0.3)
        elif model_name == LLMUtil.GPT4_0125_PREVIEW_MODEL_NAME:
            plan_json = LLMUtil.ask_gpt_4_preview(messages, temperature=0.3)
        elif model_name == LLMUtil.GPT4_1106_PREVIEW_MODEL_NAME:
            plan_json =  LLMUtil.ask_gpt4_1106_turbo_preview(messages, temperature=0.3)
        elif model_name == LLMUtil.GPT4_TURBO_PREVIEW_MODEL_NAME:
            plan_json =  LLMUtil.ask_gpt4_turbo_preview(messages, temperature=0.3)
        elif model_name == LLMUtil.GPT4_MODEL_NAME:
            plan_json = LLMUtil.ask_gpt_4_turbo(messages, temperature=0.3)
        elif model_name == LLMUtil.GPT3_5_TURBO_16K_MODEL_NAME:
            plan_json = LLMUtil.ask_gpt3_5turbo16k(messages, temperature=0.3)
        elif model_name == LLMUtil.GPT3_5_TURBO_1106_MODEL_NAME:
            plan_json =  LLMUtil.ask_gpt35_1106_turbo_preview(messages, temperature=0.3)
        elif model_name == LLMUtil.GPT3_5_TURBO_0125_MODEL_NAME:
            plan_json =  LLMUtil.ask_gpt3_5turbo_json(messages, temperature=0.3)
        elif model_name == LLMUtil.Claude3_5_MODEL_NAME:
            plan_json =  LLMUtil.ask_claude3_5(messages, temperature=0.3)
        print(plan_json)
        json_data = json.loads(plan_json)
        # print(json_data["development_plan"])
        filepath = os.path.join(repo_path, filename)
        with open(filepath, 'w') as json_file:
            json.dump(json_data, json_file, indent=2)
            logger.success(f"Saved API response to {filepath}")
    except json.decoder.JSONDecodeError as e:
        match = re.search(r"\{(?:[^{}]|(?R))*\}", plan_json, re.DOTALL)
        if match:
            json_str = match.group(0)
            print(json_str)
            try:
                data = json.loads(json_str)
                print(data)
            except json.JSONDecodeError as e:
                print(f"Failed to parse JSON: {e}")
        else:
            print("No JSON data found in the text.")
        return
    except Exception as e:
        logger.error(f"Failed to generate or save plan . Error: {e}")

 
def generate_response( project_plan, model_name):
    logger.info("Generating code planning tasks")
    messages = [{"role": "user", "content": project_plan}]
    try:
        token_count = LLMUtil.calculate_token_nums_for_prompt(project_plan)
        logger.info(f"Token count for prompt: {token_count}")
        if model_name == LLMUtil.GPT3_5_TURBO_MODEL_NAME:
            plan_json = LLMUtil.ask_gpt3_5turbo(messages, temperature=0.3)
        elif model_name == LLMUtil.GPT4_0125_PREVIEW_MODEL_NAME:
            plan_json = LLMUtil.ask_gpt_4_preview(messages, temperature=0.3)
        elif model_name == LLMUtil.GPT4_1106_PREVIEW_MODEL_NAME:
            plan_json =  LLMUtil.ask_gpt4_1106_turbo_preview(messages, temperature=0.3)
        elif model_name == LLMUtil.GPT4_TURBO_PREVIEW_MODEL_NAME:
            plan_json =  LLMUtil.ask_gpt4_turbo_preview(messages, temperature=0.3)
        elif model_name == LLMUtil.GPT4_MODEL_NAME:
            plan_json = LLMUtil.ask_gpt_4_turbo(messages, temperature=0.3)
        elif model_name == LLMUtil.GPT3_5_TURBO_16K_MODEL_NAME:
            plan_json = LLMUtil.ask_gpt3_5turbo16k(messages, temperature=0.3)
        elif model_name == LLMUtil.GPT3_5_TURBO_1106_MODEL_NAME:
            plan_json =  LLMUtil.ask_gpt35_1106_turbo_preview(messages, temperature=0.3)
        elif model_name == LLMUtil.GPT3_5_TURBO_0125_MODEL_NAME:
            plan_json =  LLMUtil.ask_gpt3_5turbo_json(messages,temperature=0.3)  
        elif model_name == LLMUtil.Claude3_5_MODEL_NAME:
            plan_json =  LLMUtil.ask_claude3_5(messages, temperature=0.3) 
        json_data = json.loads(plan_json)
        return json_data
    except Exception as e:
        logger.error(f"Failed to generate or save plan . Error: {e}")

def generate_api_inputs_and_filenames(number_of_calls, gpt_model):
    api_inputs = [f"input{i}" for i in range(1, number_of_calls + 1)]
    filenames = [f"response{i}_{gpt_model}.json" for i in range(1, number_of_calls + 1)]
    return api_inputs, filenames

def select_model(selected_model, message, temperature=0.3):
    if selected_model == LLMUtil.GPT3_5_TURBO_MODEL_NAME:
        development_json =  LLMUtil.ask_gpt3_5turbo(message, temperature=0.3)
    elif selected_model == LLMUtil.GPT4_0125_PREVIEW_MODEL_NAME:
        development_json =  LLMUtil.ask_gpt_4_preview(message, temperature=0.3)
    elif selected_model == LLMUtil.GPT4_MODEL_NAME:
        development_json =  LLMUtil.ask_gpt_4_preview(message, temperature)
    elif selected_model == LLMUtil.GPT3_5_TURBO_16K_MODEL_NAME:
        development_json =  LLMUtil.ask_gpt3_5turbo16k(message, temperature)
    elif selected_model == LLMUtil.GPT4_TURBO_PREVIEW_MODEL_NAME:
        development_json =  LLMUtil.ask_gpt4_turbo_preview(message, temperature=0.3)
    elif selected_model == LLMUtil.GPT4_1106_PREVIEW_MODEL_NAME:
        development_json =  LLMUtil.ask_gpt4_1106_turbo_preview(message, temperature=0.3)
    elif selected_model == LLMUtil.GPT3_5_TURBO_0125_MODEL_NAME:
        development_json =  LLMUtil.ask_gpt3_5turbo_json(message, temperature=0.3)
    elif selected_model == LLMUtil.Claude3_5_MODEL_NAME:
        development_json =  LLMUtil.ask_claude3_5(message, temperature=0.3)
    else:
        raise ValueError(f"Unsupported model name: {selected_model}")
    return development_json

def get_generation_code(selected_model, messages, max_attempts=5):
    attempt = 0
    logger.info("Generate Source Code.")
    while attempt < max_attempts:
        try:
            development_json = select_model(selected_model, messages)
            logger.info(LLMUtil.calculate_token_nums_for_prompt(development_json))
            print(development_json)
            json_data = json.loads(development_json)
            logger.success("Generate Source Code Success.")
            return json_data
        except json.JSONDecodeError as e:
            logger.error(f"JSON decoding failed on attempt {attempt + 1}: {str(e)}.")
            attempt += 1
    logger.error("Failed to process the message after several attempts.")
    raise Exception("Failed to process the message after several attempts.")


def get_refactor_code(selected_model, bug_message, max_attempts=10):
    attempt = 0
    logger.info("-----------Fixing Code----------------")
    while attempt < max_attempts:
        try:
            fix_code = select_model(selected_model, bug_message)
            json_data = json.loads(fix_code)
            new_code = json_data["new_version_code"]
            ast.parse(new_code)
            return new_code
        except json.JSONDecodeError as e:
            logger.error(f"JSON decoding failed on attempt {attempt + 1}: {str(e)}")
            attempt += 1
        except SyntaxError as e:
            attempt += 1
            logger.info(f"Syntax error in code")
    logger.error("Failed to generate code without pass after several attempts.")
    return "error"





def run_command(command, cwd=None, env=None):
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
            errors='replace' 
        )
        return result.stdout
    except subprocess.CalledProcessError as e:
        print(f"Error executing command: {full_command}")
        print(f"Return code: {e.returncode}")
        print(f"Output: {e.stdout}")
        print(f"Error: {e.stderr}")


def check_commands(env, command, cwd, env_vars=None):
    if env is None:
        full_command = command
    else:
        full_command = ["conda", "run", "-n", env] + command
    logger.info(full_command)
    process_env = os.environ.copy()
    if env_vars:
        process_env.update(env_vars)

    process = subprocess.Popen(full_command, cwd=cwd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    outputs = []
    while True:
        output = process.stdout.readline()
        if not output and process.poll() is not None:
            break
        if output:
            decoded_output = output.strip().decode()
            print(decoded_output)

            outputs.append(decoded_output)
            logger.info(html.escape(decoded_output))

    rc = process.poll()
    return "\n".join(outputs), rc

def log_error(message, error):
    escaped_message = html.escape(message + error)
    try:
        logger.error(escaped_message)
    except UnicodeEncodeError:
        logger.error(escaped_message.encode('utf-8').decode('utf-8'))


def check_code_pass(code):
    code = textwrap.dedent(code).strip()
    attempt_tree = 0
    try:
        tree = ast.parse(code)
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                pass_refactor = False
                for sub_node in node.body:
                    if isinstance(sub_node, (ast.Pass)):
                        pass_refactor = True
                        break
                if pass_refactor:
                    return True
        return False
    except SyntaxError as e:
        attempt_tree += 1
        print(code)
        print(e)
        log_error(f"Syntax error in code on attempt {attempt_tree}", str(e))
        return False


def filter_keywords(data, keywords):
    return {key: data[key] for key in keywords if key in data}



class ImportCollector(ast.NodeVisitor):
    def __init__(self):
        self.imports = []

    def visit_Import(self, node):
        for alias in node.names:
            import_statement = ('import', alias.name, alias.asname)
            self.imports.append(import_statement)
        self.generic_visit(node)

    def visit_ImportFrom(self, node):
        for alias in node.names:
            from_import_statement = ('from', node.module, alias.name, alias.asname)
            self.imports.append(from_import_statement)
        self.generic_visit(node)


def extract_imports_from_generated_code(generated_code):
    collector = ImportCollector()
    collector.visit(ast.parse(generated_code))
    return collector.imports

class ImportRemover(ast.NodeTransformer):
    def visit_Import(self, node):
        return None 

    def visit_ImportFrom(self, node):
        return None 

def remove_imports(code):
    tree = ast.parse(code)
    cleaner = ImportRemover()
    clean_tree = cleaner.visit(tree)
    return astunparse.unparse(clean_tree)

def fix_bracket_format(code):
    pattern = r'\[(\([^)]+\))\]'
    corrected_code = re.sub(pattern, lambda m: f"[{m.group(1)[1:-1]}]", code)
    return corrected_code

def format_imports(import_list):
    formatted_imports = []
    for imp in import_list:
        if imp[0] == 'import':
            if imp[2]:  
                formatted_imports.append(f"import {imp[1]} as {imp[2]}\n")
            else:
                formatted_imports.append(f"import {imp[1]}\n")
        elif imp[0] == 'from':
            if imp[3]:
                formatted_imports.append(f"from {imp[1]} import {imp[2]} as {imp[3]}\n")
            else:
                formatted_imports.append(f"from {imp[1]} import {imp[2]}\n")
    return formatted_imports

def add_imports_to_file(file_path, imports):
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.readlines()
    content = imports +content
    with open(file_path, 'w', encoding='utf-8') as file:
        file.writelines(content)

def update_source_files_with_imports(to_implement_funcs, dest_path):
    file_to_replacements = {}
    for func in to_implement_funcs:
        meta_info = func["meta"]
        imports = func["imports"]
        relative_file_path = meta_info['relative_path']
        file_path = os.path.join(dest_path, relative_file_path)
        if file_path not in file_to_replacements:
            file_to_replacements[file_path] = imports
        else:
            for import_line in imports:
                if import_line not in file_to_replacements[file_path]:
                    file_to_replacements[file_path].append(import_line)

    for file_path, imports in file_to_replacements.items():
        imports = [im for im in imports if "import" in im]
        with open(file_path, 'r', encoding='utf-8') as file:
            code = file.read()
        new_code = remove_imports(code)
        corrected_code = fix_bracket_format(new_code)
        full_code = '\n'.join(imports) + '\n' + corrected_code
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(full_code)


class CodeModifier(ast.NodeTransformer):
    def __init__(self, replacements=None):
        self.replacements = replacements or {}
        self.processed_keys = set()

    def visit_If(self, node):
        contains_import = any(
            isinstance(stmt, (ast.Import, ast.ImportFrom)) for stmt in node.body
        )
        if contains_import:
            print(f"Removing if statement with imports: {ast.unparse(node)}")
            return None
        return self.generic_visit(node)

    def visit_Expr(self, node):
        if isinstance(node.value, ast.Call) and isinstance(node.value.func, ast.Attribute):
            if (isinstance(node.value.func.value, ast.Attribute) and
                node.value.func.value.attr == 'path' and
                isinstance(node.value.func.value.value, ast.Name) and
                node.value.func.value.value.id == 'sys' and
                node.value.func.attr == 'append'):
                print("Removing sys.path.append statement")
                return None
        return self.generic_visit(node)

    def visit_FunctionDef(self, node):
        if hasattr(node, 'parent') and isinstance(node.parent, ast.ClassDef):
            class_name = node.parent.name
            key = f"{class_name}.{node.name}"
        else:
            key = node.name
        
        if key in self.replacements and key not in self.processed_keys:
            new_function_code = self.replacements[key][0]
            new_function_code = adjust_code_indentation(new_function_code)
            new_function_nodes = ast.parse(new_function_code).body

            for new_node in new_function_nodes:
                if isinstance(new_node, ast.FunctionDef):
                    self.processed_keys.add(key)
                    return new_node
        return self.generic_visit(node)

def adjust_code_indentation(code):
    lines = code.split('\n')
    if lines:
        indent = len(lines[0]) - len(lines[0].lstrip())
        adjusted_lines = [line[indent:] if len(line) >= indent else line for line in lines]
        return '\n'.join(adjusted_lines)
    return code



class FunctionExtractor(ast.NodeVisitor):
    def __init__(self):
        self.functions = {}
        self.current_class = None

    def visit_ClassDef(self, node):
        self.current_class = node.name
        self.generic_visit(node)
        self.current_class = None
    def visit_FunctionDef(self, node):
        if self.current_class:
            key = f"{self.current_class}.{node.name}"
        else:
            key = node.name
        self.functions[key] = node
        self.generic_visit(node)
    def visit_AsyncFunctionDef(self, node):
        self.visit_FunctionDef(node)

def get_function_code(key, source_code, ground_truth_code):
    tree = ast.parse(source_code)
    extractor = FunctionExtractor()
    extractor.visit(tree)

    if key in extractor.functions:
        function_node = extractor.functions[key]
        return ast.unparse(function_node)
    else:
        function_name = key.split(".")[-1]
        if function_name in extractor.functions:
            function_node = extractor.functions[function_name]
            return ast.unparse(function_node)
        else:
            ground_truth_tree = ast.parse(ground_truth_code)
            ground_truth_extractor = FunctionExtractor()
            ground_truth_extractor.visit(ground_truth_tree)
            if function_name in ground_truth_extractor.functions:
                function_node = ground_truth_extractor.functions[function_name]
                function_node.body = [ast.parse("pass").body[0]]  # 替换函数体为 pass
                print(ast.unparse(function_node))
                return ast.unparse(function_node)
            return None

class FunctionExtractor(ast.NodeVisitor):
    def __init__(self):
        self.functions = {}
        self.current_class = None

    def visit_ClassDef(self, node):
        self.current_class = node.name
        self.generic_visit(node)
        self.current_class = None

    def visit_FunctionDef(self, node):
        if self.current_class:
            key = f"{self.current_class}.{node.name}"
        else:
            key = node.name
        self.functions[key] = node
        self.generic_visit(node)

    def visit_AsyncFunctionDef(self, node):
        self.visit_FunctionDef(node)

class CodeModifier(ast.NodeTransformer):
    def __init__(self, replacements, pass_function_list=None):
        self.replacements = replacements
        self.pass_function_list = pass_function_list or []
        self.current_class = None
    def visit_Import(self, node):
        return None
    def visit_ImportFrom(self, node):
        return None
    def visit_If(self, node):
        contains_import = any(
            isinstance(stmt, (ast.Import, ast.ImportFrom)) for stmt in node.body
        )
        if contains_import:
            print(f"Removing if statement with imports: {ast.unparse(node)}")
            return None
        return self.generic_visit(node)
    def visit_Expr(self, node):
        if isinstance(node.value, ast.Call) and isinstance(node.value.func, ast.Attribute):
            if (isinstance(node.value.func.value, ast.Attribute) and
                node.value.func.value.attr == 'path' and
                isinstance(node.value.func.value.value, ast.Name) and
                node.value.func.value.value.id == 'sys' and
                node.value.func.attr == 'append'):
                print("Removing sys.path.append statement")
                return None
        return self.generic_visit(node)
    
    def visit_ClassDef(self, node):
        self.current_class = node.name
        self.generic_visit(node)
        self.current_class = None
        return node

    def visit_FunctionDef(self, node):
        key = self._get_key(node)

        if key in self.replacements:
            new_function_code_list = self.replacements[key]
            if isinstance(new_function_code_list, list) and new_function_code_list:
                new_function_code = new_function_code_list[0]
                new_function_code = adjust_code_indentation(new_function_code)
                new_function_nodes = ast.parse(new_function_code).body
                if len(new_function_nodes) == 1 and isinstance(new_function_nodes[0], ast.FunctionDef):
                    return new_function_nodes[0]
        if key in self.pass_function_list:
            node.body = [ast.parse("pass").body[0]]
            return node
        
        return self.generic_visit(node)

    def _get_key(self, node):
        if self.current_class:
            return f"{self.current_class}.{node.name}"
        return node.name

def replace_files(to_implement_funcs, pass_key_list, dest_path):
    file_to_replacements = {}
    file_to_imports = {}
    for func in to_implement_funcs:
        fqn = func["fqn_list"]
        meta_info = func
        imports = []
        for i in func["gen_import"]:
            if i not in imports:
                imports.append(i)

        relative_file_path = func['relative_path']
        file_path = os.path.join(dest_path, relative_file_path)

        if file_path not in file_to_imports:
            file_to_imports[file_path] = imports
        else:
            for import_line in imports:
                if import_line not in file_to_imports[file_path]:
                    file_to_imports[file_path].append(import_line)

        function_name = meta_info["fqn_list"].split("/")[-1]
        class_name = meta_info['class']
        ground_truth_code = meta_info["comment_free_code"]
        if class_name:
            class_name = class_name.split(".")[-1]
        key = f"{class_name}.{function_name}" if class_name else function_name
        if file_path not in file_to_replacements:
            file_to_replacements[file_path] = {}
        if key not in file_to_replacements[file_path]:
            file_to_replacements[file_path][key] = []
        tree = ast.parse(func["gen_code"])
        extractor = FunctionExtractor()
        extractor.visit(tree)
        sc = get_function_code(key, func["gen_code"], ground_truth_code)
        file_to_replacements[file_path][key].append(adjust_code_format(sc))

    for file_path, replacements in file_to_replacements.items():
        imports = file_to_imports.get(file_path, [])
        imports = [im for im in imports if "import" in im]
        with open(file_path, 'r', encoding='utf-8') as file:
            code = file.read()
        # new_code = remove_imports(code)
        new_tree = ast.parse(code)
        replacer = CodeModifier(replacements, pass_key_list)
        modified_tree = replacer.visit(new_tree)
        modified_code = ast.unparse(modified_tree)
        new_code = remove_imports(modified_code)
        full_code = '\n'.join(imports) + '\n' + new_code
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(full_code)

def get_key_name(meta_info):
    function_name = meta_info["fqn_list"].split("/")[-1]
    class_name = meta_info['class']
    if class_name:
        class_name = class_name.split(".")[-1]
    key = f"{class_name}.{function_name}" if class_name else function_name
    return key


class CodeModifier(ast.NodeTransformer):
    def __init__(self, replacements, pass_function_list=None):
        self.replacements = replacements
        self.pass_function_list = pass_function_list or []
        self.current_class = None

    def visit_ClassDef(self, node):
        self.current_class = node.name
        self.generic_visit(node)
        self.current_class = None
        return node

    def visit_FunctionDef(self, node):
        key = self._get_key(node)

        if key in self.replacements:
            new_function_code_list = self.replacements[key]
            if isinstance(new_function_code_list, list) and new_function_code_list:
                new_function_code = new_function_code_list[0]
                new_function_code = adjust_code_indentation(new_function_code)
                new_function_nodes = ast.parse(new_function_code).body
                if len(new_function_nodes) == 1 and isinstance(new_function_nodes[0], ast.FunctionDef):
                    return new_function_nodes[0]
        if key in self.pass_function_list:
            node.body = [ast.parse("pass").body[0]]
            return node
        
        return self.generic_visit(node)

    def _get_key(self, node):
        if self.current_class:
            return f"{self.current_class}.{node.name}"
        return node.name

def replace_files_one(to_implement_funcs, pass_key_list, dest_path):
    file_to_replacements = {}
    file_to_imports = {}
    for func in to_implement_funcs:
        fqn = func["fqn_list"]
        meta_info = func
        imports = []
        for i in func["gen_import"]:
            if i not in imports and "import" in i:
                imports.append(i)

        relative_file_path = func['relative_path']
        file_path = os.path.join(dest_path, relative_file_path)

        if file_path not in file_to_imports:
            file_to_imports[file_path] = imports
        else:
            for import_line in imports:
                if import_line not in file_to_imports[file_path]:
                    file_to_imports[file_path].append(import_line)

        function_name = meta_info["fqn_list"].split("/")[-1]
        class_name = meta_info['class']
        ground_truth_code = meta_info["comment_free_code"]
        if class_name:
            class_name = class_name.split(".")[-1]
        key = f"{class_name}.{function_name}" if class_name else function_name
        if file_path not in file_to_replacements:
            file_to_replacements[file_path] = {}
        if key not in file_to_replacements[file_path]:
            file_to_replacements[file_path][key] = []
        tree = ast.parse(func["gen_code"])
        extractor = FunctionExtractor()
        extractor.visit(tree)
        sc = get_function_code(key, func["gen_code"], ground_truth_code)
        file_to_replacements[file_path][key].append(adjust_code_format(sc))

    for file_path, replacements in file_to_replacements.items():
        with open(file_path, 'r', encoding='utf-8') as file:
            code = file.read()
        new_tree = ast.parse(code)
        replacer = CodeModifier(replacements, pass_key_list)
        modified_tree = replacer.visit(new_tree)
        modified_code = ast.unparse(modified_tree)  
        # full_code = '\n'.join(imports) + '\n' + modified_code
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(modified_code)


def get_strategy_list(strategy):
    strategy_lists = {
        "import" : ['relative_path', 'local_import', 'third_import',],
        "dataset" : [ 'relative_path','fqn_list', 'type', 'class',],
        "dataset_dep" : [ 'relative_path',"fqn_list", 'class', "categorized_dependencies"],
        "base_dep" : [ 'relative_path',"fqn_list", 'class', "categorized_dependencies", "signature"],
        "base": ['relative_path', 'fqn_list', 'type', 'class', 'signature'],
        "base_design": ['relative_path', 'fqn_list', 'type', 'class', 'signature'],
        "base_10": ['relative_path', 'fqn_list', 'type', 'class', 'signature'],
        "base_all": ['relative_path', 'fqn_list', 'type', 'class', 'signature'],
        "base_comment": ['relative_path', 'fqn_list', 'type', 'class', 'signature', 'comment'],
        "base_import": ['relative_path', 'fqn_list', 'type', 'class', 'signature', 'local_import', 'third_import'],
        "base_comment_third_import": ['relative_path', 'fqn_list', 'type', 'class', 'signature', 'comment', 'third_import'],
        "base_comment_import_dependency": ['relative_path', 'fqn_list', 'type', 'class', 'signature', 'comment', 'categorized_dependencies'],
        "test": ['relative_path', 'fqn_list', 'class', 'signature', 'comment', 'test'],
        "design": ['relative_path', 'fqn_list', 'class', 'signature', 'comment']
    }
    return strategy_lists.get(strategy, strategy_lists["base"])


#----------------------------------------implementation----------------------------------------------


def run_as_sudo():
    if os.geteuid() != 0:
        print("Re-running script with sudo")
        args = ['sudo', sys.executable] + sys.argv
        os.execlpe('sudo', *args, os.environ)

def parse_args():
    parser = argparse.ArgumentParser(description="Repository processing and code generation")
    parser.add_argument('--repo_dataset', type=str, default="repogen/data", help='Path to the repository dataset')
    parser.add_argument('--result_dir', type=str, default="repogen/results", help='Path to the results directory')
    parser.add_argument('--plan_directory', type=str, default="repogen/results/plan", help='Path to the plan directory')
    parser.add_argument('--design', type=str, default="repogen/design.json", help='Path to the design file')
    parser.add_argument('--metric_path', type=str, default="repogen/results/metric", help='Path to the metric directory')
    parser.add_argument('--current_strategy', type=str, choices=[
        'base_comment', 'base_dep', 'base_10', 'base_20', 'base_design', 
        'base_import', 'metagpt', 'chatdev', 'test', 'base_claude', 'base_gpt3.5'
    ], default='base_20', help="Choose the current strategy (default: base_20)")    
    parser.add_argument('--plan_gen', action='store_true', help='Generate plans')
    parser.add_argument('--code_gen', action='store_true', help='Generate code')
    parser.add_argument('--valid_gen', action='store_true', help='Generate validations')
    parser.add_argument('--replace_gen', action='store_true', help='Replace generated code')
    parser.add_argument('--replace_one_gen', action='store_true', help='Replace one generated code')
    parser.add_argument('--replace_gen_import', action='store_true', help='Replace generated code with imports')
    parser.add_argument('--selected_model', type=str, choices=[
            'LLMUtil.GPT4_0125_PREVIEW_MODEL_NAME', 'LLMUtil.GPT3_5_TURBO_0125_MODEL_NAME', 
            'LLMUtil.Claude3_5_MODEL_NAME', 'chatdev', 'metagpt'
        ], default='LLMUtil.GPT4_0125_PREVIEW_MODEL_NAME', help="Select the model to use (default: GPT-4 0125 preview)")

    return parser.parse_args()

def main():

    args = parse_args()
    repo_dataset = args.repo_dataset
    result_dir = args.result_dir
    plan_directory = args.plan_directory
    plan_gen = args.plan_gen
    code_gen = args.code_gen
    valid_gen = args.valid_gen
    replace_gen = args.replace_gen
    replace_one_gen = args.replace_one_gen
    replace_gen_import = args.replace_gen_import
    metric_path = args.metric_path
    design = args.design
    current_strategy = args.current_strategy
    selected_model = args.selected_model


    plan_num = 1
    function_pattern = True


    if current_strategy == "base_10":
        function_batch_size = 10
    elif current_strategy == "base_20":
        function_batch_size = 20
    else:
        function_batch_size = 5


    design_ = None
    if current_strategy == "base_design":
        project_step_implementation_generation_base = project_step_implementation_generation_base_design
        project_step_implementation_generation_base_with_init =project_step_implementation_generation_base_with_init_design
        with open(design , "r") as file:
            design_ = json.load(file)


    if selected_model == LLMUtil.Claude3_5_MODEL_NAME:
        project_plan_module_generation = project_plan_module_generation_claude
        project_plan_using_module_generation = project_plan_using_module_generation_claude
        project_step_implementation_generation_base = project_step_implementation_generation_base_claude
        project_step_implementation_generation_base_with_init = project_step_implementation_generation_base_with_init_claude
        fixed_prompt = fixed_prompt_claude


    strategy_list = get_strategy_list(current_strategy)
    
    if os.path.exists(plan_directory) == False:
        os.makedirs(plan_directory)
        
    for repo_name in os.listdir(repo_dataset):
        # if repo_name == ".pytest_cache":
        #     continue
        if current_strategy == "base_design":
            design_info = design_[repo_name]
            if design_info == "":
                continue
        if repo_name in []:
            continue

        repo_path = os.path.join(repo_dataset, repo_name)
        dest_path = os.path.join(result_dir, "repo_result" , current_strategy, selected_model, repo_name)
        test_path = os.path.join(result_dir, "repo_result" , current_strategy, selected_model)
        path_prefix = repo_path 
        logger.info(f"Getting static information for {repo_name}")
        result_dir1 = f"repogen/results/static_info/{repo_name}/merged_data.json"

        if os.path.exists(dest_path) == False:
            os.makedirs(dest_path)
        if os.path.exists(result_dir1):
            with open(result_dir1, "r") as file:
                static_info = json.load(file)
        else:
            get_static_info(repo_path)
            with open(result_dir1, "r") as file:
                static_info = json.load(file)
        logger.success(f"Static information for {repo_name} has been successfully extracted")

        doc_info = static_info["readme"]
        meta_info = static_info["functions_detail"]
        meta_info_list_with_test, third_party_libraries = meta_info["functions_detail"], meta_info["third_party_libraries"]
        if repo_name == "PyNest":
            meta_info_list = [i for i in meta_info_list_with_test if "core" in i["fqn_list"].lower() and "test" not in i["fqn_list"].lower()]
        else:
            meta_info_list = [i for i in meta_info_list_with_test if "test" not in i["fqn_list"].lower() and "config" not in i["fqn_list"].lower()]

        logger.info(f"{repo_name} includes {len(meta_info_list)} functions to be generated and {len(meta_info_list_with_test) - len(meta_info_list)} test functions")
        logger.info("Generating Code Planning tasks")
        logger.info("----------------------------------------------------")
        repository_skeleton = {}
        
        moduleid2metainfo = {}
        mm2id = {}
        for id, meta in enumerate(meta_info_list):
            meta_fl = filter_keywords(meta, get_strategy_list("dataset_dep"))
            repository_skeleton[id] = meta_fl
            moduleid2metainfo[id] = meta
            if meta["fqn_list"] not in mm2id:
                mm2id[meta["fqn_list"]] = id
            mf = filter_keywords(meta, get_strategy_list("dep"))

        for meta in meta_info_list:
            code = meta["comment_free_code"]
            print(code)
            print(len(code.splitlines()))
        
        ppmg = project_plan_module_generation
        module_file = "module.json"
        module_path = os.path.join(plan_directory, current_strategy,selected_model, repo_name, module_file)
        module_gen_path = os.path.join(plan_directory, current_strategy,selected_model, repo_name, "module_to_be_analyzed.json")


        logger.info(f"Implementing task output for {repo_name}")
        logger.info("----------------------------------------------------")

        api_inputs, filenames = generate_api_inputs_and_filenames(plan_num, selected_model)
        if plan_gen and not os.path.exists(module_path):
            plgi = ppmg.format(project_readme=doc_info,code_framework=repository_skeleton)
            generate_and_save_responses_concise(module_file, plan_directory, repo_name, selected_model, plgi, current_strategy)
        if os.path.exists(module_path):
            with open(module_path, "r") as f:
                module_generation_data =  json.load(f)
        if  plan_gen and not os.path.exists(module_gen_path):
            modules_list = module_generation_data["Modules"]
            development_order = module_generation_data["development_order"]
            plan_module_response = []
            for module_name in development_order:
                for module in modules_list:
                    if module_name == module["Module"]:
                        ppumg = project_plan_using_module_generation
                        ppumg = ppumg.format(project_readme = doc_info,code_framework=repository_skeleton, module_to_be_analyzed=module)
                        plan_module_response.append(generate_response(ppumg, selected_model))
            with open(module_gen_path, "w") as f:
                json.dump(plan_module_response, f, indent=4)
        with open(module_gen_path, "r") as f:
            plan_module_response = json.load(f)

        new_task_id = 0
        consolidated_tasks = []
        key_cov = set()
        for module in plan_module_response:
            if not module:
                continue
            for module_name, tasks in module.items():
                if type(tasks) == str:
                    continue
                for task in tasks:
                    task["task_id"] = new_task_id
                    new_task_id += 1
                    task["dependency"] = [dep for dep in task["dependency"]]
                    key_id = task["key_id"]
                    key_cov.add(key_id)
                    consolidated_tasks.append(task)
        not_cov_id = [i for i in repository_skeleton.keys() if i not in key_cov]
        logger.info(f"{repo_name} plans has been successfully generated with {len(not_cov_id)} not coverage")
        for i in not_cov_id:
            task = {}
            task["task_id"] = new_task_id
            new_task_id += 1
            task["key_id"] = i
            task["dependency"] = []
            consolidated_tasks.append(task)
        logger.info(f"{repo_name} plans complete done")



        code_context = [(meta["fqn_list"], meta["signature"]) for meta in meta_info_list]
        global_implementation_plan = []
        strategy_dir = os.path.join(plan_directory, current_strategy, selected_model, repo_name)
        os.makedirs(strategy_dir, exist_ok=True)
        code_result_path = os.path.join(strategy_dir, "result.json")

        class_init_info = {}
        init_list = []
        no_init_list = []
        for task_dict in consolidated_tasks:
            task_id = task_dict["key_id"]
            meta = moduleid2metainfo[task_id]
            signature = meta["signature"]
            relative_path = meta["relative_path"]
            cl = meta["class"]
            fqn = meta["fqn_list"].lower()
            if "__init__(" in signature and cl:
                init_list.append(task_dict)
                class_varibale = get_class_variables(path_prefix, relative_path, cl)
                class_init_info[cl] = {"init_code" : "" ,"class_variable": class_varibale}
            else:

                no_init_list.append(task_dict)

        for task_dict in consolidated_tasks:
            task_id = task_dict["key_id"]
            meta = moduleid2metainfo[task_id]
            cl = meta["class"]
            if cl and cl not in class_init_info:
                class_varibale = get_class_variables(path_prefix, relative_path, cl)
                class_init_info[cl] = {"class_variable": class_varibale}
                print(cl)



        if code_gen == True and (not os.path.exists(code_result_path)):
            logger.info("Starting distributed task generation")
            logger.info("--------------------------------------")
            logger.info(f"{repo_name} -- Task Begin")
            logger.info(init_list)
            logger.info(f"{repo_name} -- Generating __init__ functions first")
            init_response = {}
            for i in tqdm(range(0, len(init_list), function_batch_size), desc=f"{repo_name} -- Task in process"):
                psi = project_step_implementation_generation_base
                batch = init_list[i:i + function_batch_size]
                code_framework = []
                clas_ = []
                for step in batch:
                    task_id = step["key_id"]
                    step["task_id"] = step["key_id"]
                    meta = moduleid2metainfo[task_id]
                    cl = meta["class"]
                    if cl not in clas_:
                        clas_.append(cl)
                    cv = class_init_info[cl]["class_variable"]
                    step["variable"] = [
                        {"local_variable in file" : meta["local_variables"]},
                        {"class variable" : cv}
                        ]
                    fqn = meta["fqn_list"]
                    step["detail_information"] = filter_keywords(meta, strategy_list)
                    refer_id_list = step["dependency"]
                    refer_meta_list = []
                    print(refer_id_list)
                    for refer_id in refer_id_list:
                        if not refer_id:
                            continue
                        refer_meta = moduleid2metainfo[refer_id]
                        filter_info = filter_keywords(refer_meta, strategy_list)
                        refer_meta_list.append(filter_info)
                    step["dependency_information"] = refer_meta_list
                    code_framework.append(step)
                if current_strategy == "base_design":
                    logger.info("yes, in base design")
                    psi = psi.format(
                            project_readme=double_braces(doc_info),
                            code_context=code_context,
                            code_framework = code_framework,
                            work_env = third_party_libraries,
                            design_info = design_info
                        )
                else:
                    psi = psi.format(
                            project_readme=double_braces(doc_info),
                            code_context=code_context,
                            code_framework = code_framework,
                            work_env = third_party_libraries
                    )
                logger.info(f"{len(LLMUtil.get_tokens(psi))} tokens in project implementation plan request")
                messages = [{"role": "user", "content": psi}]
                code_result = get_generation_code(selected_model, messages)
                for clas in clas_:
                    for iic in code_result["implementation_plan"]:
                        if clas.split(".")[-1] in iic["fqn"]:
                            print("match init")
                            class_init_info[clas]["init_code"] = iic["code"]
                implementation_plan = code_result["implementation_plan"]
                global_implementation_plan.extend(implementation_plan)
                logger.info("__init__ functions generation completed")

            for i in tqdm(range(0, len(no_init_list), function_batch_size), desc=f"{repo_name} -- Task in process"):
                psi = project_step_implementation_generation_base_with_init
                batch = no_init_list[i:i + function_batch_size]
                code_framework = []
                init_context = {}
                for step in batch:
                    task_id = step["key_id"]
                    step["task_id"] = step["key_id"]
                    meta = moduleid2metainfo[task_id]
                    cl = meta["class"]
                    if cl in class_init_info and "init_code" in class_init_info[cl]:
                        cv = class_init_info[cl]["class_variable"]
                        ci = class_init_info[cl]["init_code"]
                    elif cl in class_init_info and "init_code" not in class_init_info[cl]:
                        cv = class_init_info[cl]["class_variable"]
                        ci = "no init in class"
                    else:
                        cv = "no init in class"
                        ci = None
                    step["variable"] = [
                                {"local_variable in file" : meta["local_variables"]},
                                {"class variable" : cv}
                                ]
                    fqn = meta["fqn_list"]
                    init_context[fqn] = ci
                    step["detail_information"] = filter_keywords(meta, strategy_list)
                    refer_id_list = step["dependency"]
                    refer_meta_list = []
                    for refer_id in refer_id_list:
                        if not refer_id or refer_id not in moduleid2metainfo:
                            continue
                        refer_meta = moduleid2metainfo[refer_id]
                        filter_info = filter_keywords(refer_meta, strategy_list)
                        refer_meta_list.append(filter_info)
                    step["dependency_information"] = refer_meta_list
                    code_framework.append(step)
                if current_strategy == "base_design":
                    psi = psi.format(
                        project_readme=double_braces(doc_info),
                        code_context=code_context,
                        code_framework = code_framework,
                        work_env = third_party_libraries,
                        init_context = init_context,
                        design_info = design_info
                        )
                else:
                    psi = psi.format(
                        project_readme=double_braces(doc_info),
                        code_context=code_context,
                        code_framework = code_framework,
                        work_env = third_party_libraries,
                        init_context = init_context
                        )

                logger.info(f"{len(LLMUtil.get_tokens(psi))} tokens in project implementation plan request")
                messages = [{"role": "user", "content": psi}]
                code_result = get_generation_code(messages)
                implementation_plan = code_result["implementation_plan"]
                global_implementation_plan.extend(implementation_plan)
            with open(code_result_path, "w") as f:
                json.dump({"implementation": global_implementation_plan}, f, indent=4)

            logger.info(f"{repo_name} -- Task generation completed and saved to {code_result_path} -- {len(global_implementation_plan)}")



        if not os.path.exists(code_result_path):
            continue
        with open(code_result_path, "r", encoding="utf-8") as f:
            code_result = json.load(f)

        code_result_path = os.path.join(strategy_dir, "result_fixed.json")
        if valid_gen == True and not os.path.exists(code_result_path):
            logger.info("---------Entering Evaluation Phase------------")
            logger.info("Parsing output information")
            implementation_list = code_result["implementation"]
            print(len(implementation_list))
            logger.info("Initial code generation successful, proceeding with code verification and refactoring")
            logger.info("----------------------------------------------------")
            fqn1_set = set()
            result = []
            for clas_ in meta_info_list:
                if clas_["fqn_list"] not in fqn1_set:
                    fqn1_set.add(clas_["fqn_list"])
                    clas_["cov"] = False
                    clas_["syn"] = False
                    clas_["keyid"] = -1
                    for i in implementation_list:
                        if i["fqn"].lower() == clas_["fqn_list"].lower():
                            clas_["cov"] = True
                            clas_["keyid"] = i["key_id"]
                            clas_["gen_code"] = i["code"]
                            clas_["gen_import"] = i["imports"]
                    result.append(clas_)
            no_cov = [clas_["keyid"] for clas_ in result if clas_["cov"] == False]
            logger.info(f"{len(no_cov)} functions were not effectively covered")

            syntaxerror_id_list = []
            for code_dict in implementation_list:
                code_id = code_dict["key_id"]
                source_code = code_dict["code"]
                try:
                    ast.parse(source_code)
                except SyntaxError as e:
                    print(f"Syntax error in code ID {code_id}: {e}")
                    error_message = str(e)
                    fp = fixed_prompt
                    fp = fp.format(
                        code_to_be_fixed = source_code,
                        error_description = error_message
                    )
                    messages = [{"role": "user", "content": fp}]
                    fix_code = get_refactor_code(selected_model, messages)
                    if "error" != fix_code:
                        syntaxerror_id_list.append(code_id)
                        logger.info("Fixing Success")
                        code_dict["code"] = fix_code
                    else:
                        syntaxerror_id_list.append(code_id)
            for si in syntaxerror_id_list:
                for clas_ in result:
                    if clas_["keyid"] == si:
                        clas_["syn"] = True
            syn_error = [clas_["keyid"] for clas_ in result if clas_["syn"] == True]
            print(len(syn_error))
            if not os.path.exists(code_result_path):
                with open(code_result_path, "w") as f:
                    json.dump({"implementation": result}, f, indent=4)
            continue

                

        if replace_gen == True:
            code_result_path = os.path.join(strategy_dir, "result_fixed.json")
            with open(code_result_path, "r", encoding="utf-8") as f:
                code_result = json.load(f)
            logger.info("Executing code replacement task")
            implementation_list = code_result["implementation"]
            total_problem = len(implementation_list)
            no_cov = [clas_ for clas_ in implementation_list if clas_["cov"] == False]
            syn_cov = [clas_ for clas_ in implementation_list if clas_["syn"] == True]
            to_replace_list = []
            pass_list = []
            for clas_ in implementation_list:
                if clas_["cov"] == False or clas_["syn"] == True:
                    pass_list.append(clas_)
                else:
                    to_replace_list.append(clas_)

            pass_key_list = [get_key_name(i) for i in pass_list]
            to_replace_key_list = [get_key_name(i) for i in to_replace_list]
            copy_project_structure(path_prefix, dest_path)


            strategy_dir = os.path.join(metric_path, current_strategy, selected_model)
            code_result_path = os.path.join(strategy_dir, "sum_metric.json")
            if os.path.exists(code_result_path):
                with open(code_result_path) as f:
                    dict_res = json.load(f)
                if repo_name in dict_res:
                    continue



            replace_files(to_replace_list, pass_key_list,  dest_path)
            logger.success(f"Successfully added to the {repo_name} repository")
            logger.info("----------------------------------------------------")
            logger.info(f"Running tests for {repo_name}")
            res = run_test(test_path, repo_name)
            logger.info("---------------------------------------------------")
            logger.info(f"Tests for {repo_name} completed")
            logger.info("---------------------------------------------------")
            strategy_dir = os.path.join(metric_path, current_strategy, selected_model)
            if not os.path.exists(strategy_dir):
                os.makedirs(strategy_dir)
            code_result_path = os.path.join(strategy_dir, "sum_metric.json")
            if os.path.exists(code_result_path):
                with open(code_result_path) as f:
                    dict_res = json.load(f)
            else:
                dict_res = {}
            dict_res[repo_name] = [
                {"pass" : len(res["pass"]) },
                {"fail" : len(res["fail"])},
                {"error" : len(res["error"]) },
                {"result" : res["result"]}
                ]
            with open(code_result_path, "w") as f:
                f.write(json.dumps(dict_res, indent=4))
            print(code_result_path)


        if replace_gen_import == True:
            code_result_path = os.path.join(strategy_dir, "result_fixed.json")
            print(path_prefix)
            logger.info("----------------------------------------------------")
            logger.info("Adding reference information")

            with open(code_result_path, "r", encoding="utf-8") as f:
                code_result = json.load(f)
            logger.info("Executing code replacement task")
            implementation_list = code_result["implementation"]

            total_problem = len(implementation_list)
            no_cov = [clas_ for clas_ in implementation_list if clas_["cov"] == False]
            syn_cov = [clas_ for clas_ in implementation_list if clas_["syn"] == True]
            to_replace_list = []
            pass_list = []
            for clas_ in implementation_list:
                if clas_["cov"] == False or clas_["syn"] == True:
                    pass_list.append(clas_)
                else:
                    to_replace_list.append(clas_)

            pass_key_list = [get_key_name(i) for i in pass_list]
            to_replace_key_list = [get_key_name(i) for i in to_replace_list]
            handle_docker_setup_before_copy(repo_name, test_path)
            

            copy_project_structure(path_prefix, dest_path)
            strategy_dir = os.path.join(metric_path, current_strategy, selected_model)
            code_result_path = os.path.join(strategy_dir, "sum_metric_import.json")
            if os.path.exists(code_result_path):
                with open(code_result_path) as f:
                    dict_res = json.load(f)
                if repo_name in dict_res:
                    continue




            replace_files_one(to_replace_list, pass_key_list,  dest_path)
            logger.success(f"Successfully added to the {repo_name} repository")
            logger.info("----------------------------------------------------")
            logger.info(f"Running tests for {repo_name}")
            res = run_test(test_path, repo_name)
            logger.info("---------------------------------------------------")
            logger.info(f"Tests for {repo_name} completed")


            logger.info("---------------------------------------------------")
            strategy_dir = os.path.join(metric_path, current_strategy, selected_model)
            if not os.path.exists(strategy_dir):
                os.makedirs(strategy_dir)
            code_result_path = os.path.join(strategy_dir, "sum_metric_import.json")
            if os.path.exists(code_result_path):
                with open(code_result_path) as f:
                    dict_res = json.load(f)
            else:
                dict_res = {}
            dict_res[repo_name] = [
                {"pass" : len(res["pass"]) },
                {"fail" : len(res["fail"])},
                {"error" : len(res["error"]) },
                {"result" : res["result"]}
                ]
            with open(code_result_path, "w") as f:
                f.write(json.dumps(dict_res, indent=4))
            print(code_result_path)



        if replace_one_gen == True:
            code_result_path = os.path.join(strategy_dir, "result_fixed.json")
            logger.info("----------------------------------------------------")
            with open(code_result_path, "r", encoding="utf-8") as f:
                code_result = json.load(f)
            logger.info("Executing code replacement task")
            implementation_list = code_result["implementation"]
            total_problem = len(implementation_list)
            no_cov = [clas_ for clas_ in implementation_list if clas_["cov"] == False or clas_["syn"] == True]
            wrong_num = 0
            wrong_num += len(no_cov)

            to_replace_list = []
            pass_list = []
            for clas_ in implementation_list:
                if clas_["cov"] == False or clas_["syn"] == True:
                    pass_list.append(clas_)
                else:
                    to_replace_list.append(clas_)
            pfe = []
            strategy_dir = os.path.join(metric_path, current_strategy, selected_model)
            code_result_path = os.path.join(strategy_dir, "metric_funcional.json")
            if os.path.exists(code_result_path):
                with open(code_result_path) as f:
                    dict_res = json.load(f)
                    if repo_name in dict_res:
                        continue
            for i in tqdm(to_replace_list, desc=f"{repo_name} -- Functional Test in process"):
                handle_docker_setup_before_copy(repo_name, test_path)
                trl = [i]
                copy_project_structure(path_prefix, dest_path)
                replace_files_one(trl, [],  dest_path)
                res = run_test(test_path, repo_name)
                print(len(res["pass"]), len(res["fail"]), len(res["error"]))
                if len(res["fail"]) > 0 or len(res["error"]) > 0:
                    wrong_num += 1
                else:
                    print("function pass all test")
            strategy_dir = os.path.join(metric_path, current_strategy, selected_model)
            code_result_path = os.path.join(strategy_dir, "metric_funcional.json")
            if not os.path.exists(strategy_dir):
                os.makedirs(strategy_dir)
            if os.path.exists(code_result_path):
                with open(code_result_path) as f:
                    dict_res = json.load(f)
            else:
                dict_res = {}
            dict_res[repo_name] = [
                {"all_num" : total_problem },
                {"success" : total_problem - wrong_num },
                {"wrong" : wrong_num },
                ]
            with open(code_result_path, "w") as f:
                f.write(json.dumps(dict_res, indent=4))











if __name__ == "__main__":
    main()

