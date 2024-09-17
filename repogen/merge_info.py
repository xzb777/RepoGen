import os
import subprocess
import json
import sys

def run_script_in_conda_env(env_name, script_path, repo_path, output_path):
    command = f"conda run -n {env_name} python {script_path} {repo_path} {output_path}"
    print(f"Running command: {command}")
    try:
        result = subprocess.run(command, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print("stdout:", result.stdout.decode())
        print("stderr:", result.stderr.decode())
    except subprocess.CalledProcessError as e:
        print("Error running command:", command)
        print("stdout:", e.stdout.decode())
        print("stderr:", e.stderr.decode())
        raise

def read_json_file(filepath):
    with open(filepath, 'r') as f:
        return json.load(f)

def get_readme_content(repo_path):
    readme_file = os.path.join(repo_path, "README.md")
    if not os.path.isfile(readme_file):
        raise FileNotFoundError(f"README.md file not found in the repository path: {repo_path}")
    with open(readme_file, 'r', encoding='utf-8') as file:
        content = file.read()
    return content

def get_static_info(repo_path, other_agent = None):
    static_info = "static_info"
    depfinder = "depfinder"
    function_base_script = "repogen/main/get_meta_info.py"
    repo_structure_script = "repogen/main/get_depedency.py"
    repo_name = os.path.basename(repo_path.rstrip('/'))
    result_dir = f"repogen/results/static_info/{repo_name}"
    if other_agent:
        result_dir = f"repogen/results/static_info/{other_agent}/{repo_name}"
    function_base_output = f"{result_dir}/function_base_data.json"
    repo_structure_output = f"{result_dir}/repo_structure_data.json"
    os.makedirs(result_dir, exist_ok=True)
    run_script_in_conda_env(static_info, function_base_script, repo_path, function_base_output)
    run_script_in_conda_env(depfinder, repo_structure_script, repo_path, repo_structure_output)
    function_base_data = read_json_file(function_base_output)
    repo_structure_data = read_json_file(repo_structure_output)
    readme_data = get_readme_content(repo_path)
    repogen = get_raw_code(repo_path, function_base_data, repo_structure_data)
    for function_detail in repogen["functions_detail"]:
        categorized_dependencies = categorize_dependencies(function_detail, repo_structure_data)
        function_detail["categorized_dependencies"] = categorized_dependencies
    merged_data = {
        "function_base": function_base_data,
        "repo_structure": repo_structure_data,
        "readme": readme_data,
        "functions_detail" : repogen
    }
    merged_output = f"{result_dir}/merged_data.json"
    with open(merged_output, 'w') as f:
        json.dump(merged_data, f, indent=4)

def get_raw_code(repo_path, content, repo_structure_data):
    repo_structure_dict = {item["Path"]: item for item in repo_structure_data.values()}
    path_dict = content['file_path']
    rl_path_dict = content["relative_file_path"]
    fqn_list = content["fully_qualified_name"]
    function_name_list = content["function_name"]
    signature_list = content["function signature"]
    raw_source_code = content["raw_source_code"]
    comment_free_code = content["comment_free_source_code"]
    class_list = content["class"]
    comment_list = content["comment"]
    local_variables_list = content["local variables"]
    is_empty_function = content["is_empty_function"]
    startlineno = content["start_lineno"]
    endlineno = content["end_lineno"]


    third_party_libraries = content["third_party_libraries"]
    local_import = content['local_import_FQNs']
    third_import = content['third_party_FQNs']
    functions_details = []
    for index, signature in enumerate(signature_list):
        class_name = class_list[index] if index < len(class_list) else None
        local_variables = local_variables_list[index] if index < len(local_variables_list) else {}
        fqn = fqn_list[index]
        repo_structure_item = repo_structure_dict.get(fqn.replace(repo_path + "/", ""))
        third_import_infile = []
        local_import_infile = []
        for li in local_import:
            if li[0] in fqn:
                local_import_infile.append(li)
        for ti in third_import:
            if ti[0] in fqn:
                third_import_infile.append(ti)
        function_detail = {
            "path": path_dict[index],
            "relative_path" : rl_path_dict[index],
            "fqn_list": fqn,
            "class": class_name,
            "signature": signature,
            "comment": comment_list[index],
            "comment_free_code": comment_free_code[index],
            "start_lineno": startlineno[index],
            "end_lineno": endlineno[index],
            "local_variables": local_variables,
            "Type": repo_structure_item.get("Type") if repo_structure_item else None,
            "Dependencies": repo_structure_item.get("Dependencies") if repo_structure_item else None,
            "local_import": local_import_infile,
            "third_import": third_import_infile,       
            "local_variables": local_variables,
        }
        functions_details.append(function_detail)

    code_structure = {
        "functions_detail": functions_details,
        "third_party_libraries": third_party_libraries,
    }

    return code_structure



def categorize_dependencies(function_detail, repo_structure_dict):
    dependencies = function_detail.get("Dependencies", [])
    categorized_dependencies = {
        "Intra-class Dependency": [],
        "Intra-file Dependency": [],
        "Cross-file Dependency": [],
        "Class Dependency": []
    }
    if dependencies:
        for dep_id in dependencies:
            dep_detail = repo_structure_dict.get(str(dep_id))
            if not dep_detail:
                continue

            dep_fqn = dep_detail["Path"]
            dep_class = dep_detail["Type"] == "ClassDef"
            dep_file = dep_fqn.split(".py")[0] + ".py"
            function_file = function_detail["relative_path"].split(".py")[0] + ".py"
            
            
            dep_infile = dep_fqn.split(".py/")[1].split("/")
            fd_infile = function_detail["fqn_list"].split(".py/")[1].split("/")
            intra_flag = False
            if len(dep_infile) >=2 and len(fd_infile) >=2 and dep_infile[:-1] == fd_infile[:-1]:
                intra_flag = True
        
            if dep_class:
                categorized_dependencies["Class Dependency"].append(dep_fqn)
            elif intra_flag:
                categorized_dependencies["Intra-class Dependency"].append(dep_fqn)
            elif dep_file == function_file:
                categorized_dependencies["Intra-file Dependency"].append(dep_fqn)
            else:
                categorized_dependencies["Cross-file Dependency"].append(dep_fqn)

    return categorized_dependencies

