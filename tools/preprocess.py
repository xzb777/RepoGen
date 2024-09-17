import os
from utils.file_util import FileUtil
from utils.code_util import CodeUtil
from utils.FunctionExtractor import extract_function_info
from utils.LocalInfoExtractor import get_variables_from_file
import pandas as pd
import tqdm

class FunctionBaseConstruction:
    def get_third_party_libraries(self, directory, function_base):
        local_repo_code_FQNs = function_base['fully_qualified_name'].tolist()
        all_fqn_module_names = []
        for local_repo_code_FQN in local_repo_code_FQNs:
            module_name = local_repo_code_FQN.split('.')[0]
            all_fqn_module_names.append(module_name)
        all_module_names = FileUtil.all_module_names(directory)
        all_module_names = list(set(all_fqn_module_names + all_module_names))
        all_import_statements = CodeUtil.all_import_statements(directory)
        all_import_exact_statements = CodeUtil.all_import_statements_new(directory)
        local_fqns = [i.replace(".py", "").replace("/", ".") for i in local_repo_code_FQNs]
        local_import_FQNs = []
        third_party_FQNs = []
        for file_path, import_statement, import_fqn in all_import_exact_statements:
            file_path = os.path.relpath(file_path, directory)
            flag = False
            for local_module in local_fqns:
                if local_module.startswith(import_fqn):
                    print(import_fqn)
                    print(local_module)
                    local_import_FQNs.append([file_path, import_statement, import_fqn])
                    flag = True
                    break
            if flag:
                continue
            else:
                third_party_FQNs.append([file_path, import_statement, import_fqn])
        third_party_libraries = []
        for _, _, FQN in third_party_FQNs:
            third_party_libraries.append(FQN.split('.')[0])
        third_party_libraries = list(set(third_party_libraries) - set(all_module_names))
        return local_import_FQNs, third_party_FQNs, third_party_libraries



    def extract_basic_function_base(self, directory):
        dict_function_base = {'repo name': [], 'file_path': [], 'relative_file_path': [], 'fully_qualified_name': [], 'function_name': [],'function signature': [], 'raw_source_code': [],'comment_free_source_code': [], 'class': [], 'is_empty_function': [],
'comment': [], 'local variables': [], "start_lineno" : [], "end_lineno" : []}
        py_files = FileUtil.all_py_files(directory)
        all_files_num = FileUtil.all_files_num(directory)
        repo_name = directory.split('/')[-1]
        for py_file in tqdm.tqdm(py_files, total=all_files_num, desc="Extracting function base..."):
            variables = get_variables_from_file(py_file)
            functions_info = extract_function_info(py_file)
            for function_info in functions_info:
                function_name = function_info['name']
                raw_source_code = function_info['source']
                comment_free_source_code = CodeUtil.remove_comments(raw_source_code)
                is_empty = CodeUtil.is_body_empty_or_only_pass(comment_free_source_code)
                class_name = function_info['class']
                start_lineno = function_info['start_lineno']
                end_lineno = function_info['end_lineno']
                function_signature = function_info['signature']
                comment = function_info['docstring']
                dict_function_base['file_path'].append(py_file)
                relative_file_path = os.path.relpath(py_file, directory).replace('\\', '/')
                module_FQN = relative_file_path
                if class_name == None:
                    fully_qualified_name = module_FQN + '/' + function_name
                else:
                    fully_qualified_name = module_FQN + '/' + class_name + '/' + function_name
                    class_name = module_FQN + '.' + class_name
                dict_function_base['start_lineno'].append(start_lineno)
                dict_function_base['end_lineno'].append(end_lineno)
                dict_function_base['repo name'].append(repo_name)
                dict_function_base['relative_file_path'].append(relative_file_path)
                dict_function_base['fully_qualified_name'].append(fully_qualified_name)
                dict_function_base['function_name'].append(function_name)
                dict_function_base['raw_source_code'].append(raw_source_code)
                dict_function_base['class'].append(class_name)
                dict_function_base['comment_free_source_code'].append(comment_free_source_code)
                dict_function_base['function signature'].append(function_signature)
                dict_function_base['comment'].append(comment)
                dict_function_base['local variables'].append(variables)
                dict_function_base['is_empty_function'].append(is_empty)
        df_function_base = pd.DataFrame(dict_function_base)
        return df_function_base, dict_function_base
    
    def extract_function_base(self, directory):
        function_base, dict_function_base = self.extract_basic_function_base(directory)
        local_import_FQNs, third_party_FQNs, third_party_libraries = self.get_third_party_libraries(directory, function_base)
        dict_function_base['local_import_FQNs'] = local_import_FQNs
        dict_function_base['third_party_FQNs'] = third_party_FQNs
        dict_function_base['third_party_libraries'] = third_party_libraries
        return dict_function_base

