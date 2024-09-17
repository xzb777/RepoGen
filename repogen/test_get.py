import os
import sys
import subprocess
import pytest
from tqdm import tqdm
import json

# repository to conda envrionment
def load_config(config_file):
    with open(config_file, 'r') as f:
        return json.load(f)


env_mapping = {
    "django-pony-express": "ponyexpress",
    "reverse_argparse": "reverse_argparse",
    "PyNest": "reverse_argparse",
    "SantorinAI": "reverse_argparse",
    "maccarone": "maccarone",
    "ufomerge": "ufomerge",
    "constrainedlr": "constrainedlr",
    "translategram": "translategram",
    "cpu_simulator": "reverse_argparse",
    "sphecerix": "sphecerix",
    "alembic-postgresql-enum": None,
    "postgres-tq": None
}

def run_specific_test(repo_name, dest_path, test_case):
    env = None
    vir = env_mapping[repo_name]
    if repo_name == "django-pony-express":
        cwd = f'{dest_path}/{repo_name}'
        full_command = ["conda", "run", "-n", vir] + ['pytest', '--ds', 'settings', test_case]
    elif repo_name in ["reverse_argparse", "PyNest", "SantorinAI", "translategram", "sphecerix"]:
        cwd = f'{dest_path}/{repo_name}'
        full_command = ["conda", "run", "-n", vir] + ['pytest', test_case]
    elif repo_name == "maccarone":
        repo_path = f"{dest_path}/{repo_name}/src"
        env = os.environ.copy()
        env['PYTHONPATH'] = repo_path
        env_vars = {
                "OPENAI_API_KEY": os.getenv("OPENAI_API_KEY"), 
                "OPENAI_API_Base": os.getenv("OPENAI_API_Base")
            } 
        if env_vars:
            env.update(env_vars)
        cwd = f'{dest_path}/{repo_name}/src'
        full_command = ["conda", "run", "-n", vir] + ['pytest', test_case]
    elif repo_name == "ufomerge":
        cwd = f'{dest_path}/{repo_name}'
        env = os.environ.copy()
        env['PYTHONPATH'] = cwd
        full_command = ["conda", "run", "-n", vir] + ['pytest', test_case]
    elif repo_name == "constrainedlr":
        cwd = f'{dest_path}'
        full_command = ["conda", "run", "-n", vir] + ['pytest', test_case]
    elif repo_name == "postgres-tq":
        cwd = f'{dest_path}/{repo_name}'
        full_command =  ["pdm", "run", "make", "test", "TEST=" + test_case]
    elif repo_name == "alembic-postgresql-enum":
        cwd = f'{dest_path}/{repo_name}'
        env = os.environ.copy()
        env['PYTEST_ARGS'] = f"{test_case}"
        full_command = ["docker-compose", "run", "run-tests"]
    elif repo_name in ["cpu_simulator"]:
        cwd = f'{dest_path}/{repo_name}'
        full_command = ["python", "-m", "unittest", test_case]


    if env:
        process = subprocess.Popen(full_command, cwd=cwd, env=env, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    else:
        process = subprocess.Popen(full_command, cwd=cwd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    outputs = []
    while True:
        output = process.stdout.readline()
        if not output and process.poll() is not None:
            break
        if output:
            decoded_output = output.strip().decode()
            outputs.append(decoded_output)
    rc = process.poll()
    return "\n".join(outputs), rc

def handle_docker_setup(repo_name, dest_path):
    cwd = f'{dest_path}/{repo_name}'
    if repo_name in ["alembic-postgresql-enum"]:
        subprocess.run(["docker-compose", "down"], cwd=cwd)
        subprocess.run(["docker-compose", "build", "--no-cache"], cwd=cwd)
        subprocess.run(["docker-compose", "up", "-d"], cwd=cwd)
    if repo_name in ["postgres-tq"]:
        subprocess.run(["docker", "rm", "-f", "postgres-tq-container"], cwd=cwd)
        subprocess.run(["make", "run-postgres"], cwd=cwd)

def handle_docker_setup_before_copy(repo_name, dest_path):
    cwd = f'{dest_path}/{repo_name}'
    if repo_name in ["alembic-postgresql-enum"]:
        subprocess.run(["docker-compose", "down"], cwd=cwd)
        # subprocess.run(["docker-compose", "build", "--no-cache"], cwd=cwd)
        # subprocess.run(["docker-compose", "up", "-d"], cwd=cwd)
    if repo_name in ["postgres-tq"]:
        subprocess.run(["docker", "rm", "-f", "postgres-tq-container"], cwd=cwd)
        # subprocess.run(["make", "run-postgres"], cwd=cwd)

def run_test(config):
    dest_path = config["dest_path"]
    repo_name = config["repo_name"]
    test_case_file = config["test_case_file"]
    handle_docker_setup(repo_name, dest_path)
    tc = load_config(test_case_file)
    test_case_statement = tc[repo_name]
    dict_res1= {
        "pass": [],
        "error": [],
        "fail": [],
        "result": []
    }
    for test_case in tqdm(test_case_statement, desc= f"{repo_name} testing"):
        try:
            result, _ = run_specific_test(repo_name, dest_path, test_case)
            if "1 passed" in result or (repo_name == "cpu_simulator" and "ok" in result.lower()):
                dict_res1["pass"].append(test_case)
            elif "1 failed" in result.lower() or (repo_name == "cpu_simulator" and "fail" in result.lower()):
                dict_res1["fail"].append(test_case)
                break
            elif "1 error" in result.lower() or (repo_name == "cpu_simulator" and "error" in result.lower()):
                dict_res1["error"].append(test_case)
                break
            else:
                dict_res1["error"].append(test_case)
                break
            dict_res1["result"].append(result)
        except Exception as e:
            # print(f"Error running test {test_case}: {str(e)}")
            dict_res1["error"].append(test_case)
            dict_res1["result"].append(str(e))
    return dict_res1

if __name__ == "__main__":
    # example of running tests for a specific repo
    dest_path = "repogen/results/repo_result/base/gpt-4-0125-preview" 
    # generated repo path using repogen with gpt-4-0125-preview
    repo_name = "sphecerix"
    test_case_file = "repogen/results/log/test_case.json"
    config = {
        "dest_path": dest_path,
        "repo_name": repo_name,
        "test_case_file": test_case_file
    }
    res = run_test(config)
    dict_res = {}
    dict_res[repo_name] = [
        {"pass" : len(res["pass"]) },
        {"fail" : len(res["fail"])},
        {"error" : len(res["error"]) }
        ]
    print(dict_res)



    repo_list = ['ufomerge', 'translategram', 'sphecerix', 'postgres-tq', 'cpu_simulator', 'django-pony-express', 'reverse_argparse', 'constrainedlr', 'maccarone', 'SantorinAI', 'alembic-postgresql-enum', 'PyNest']



