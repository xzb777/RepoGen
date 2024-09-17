
project_plan_module_generation = """
You are an expert software architect. Your task is to analyze a given code repository and divide it into distinct, functionally coherent modules. The analysis should identify which components belong to each module, based on their functionality and interdependencies. 

**Your Task**:
1. You should divide the repository into distinct, coherent modules.
2. Each module has a certain id list in json output which contain corresponding id in repository skeleton.
3. Provide the final list of modules in the order they should be developed, based on the dependencies and logical progression of the project.

**Project Readme**:
{project_readme}

**Repository Skeleton**:
{code_framework}


**Output_example**:
{{
  "Modules": [
    {{
      "Module": "Module Core",
      "key_ids": [8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, ]
    }},
    {{
      "Module": "Factory",
      "key_ids": [6, 7]
    }},
    ...
  ]
  {{
  "development_order": [
    "Network Core",
    "Factory",
    ...
  ]
}}
"""

project_plan_module_generation_claude = """
You are an expert software architect. Your task is to analyze a given code repository and divide it into distinct, functionally coherent modules. The analysis should identify which components belong to each module, based on their functionality and interdependencies. 

**Your Task**:
1. You should divide the repository into distinct, coherent modules.
2. Each module has a certain id list in json output which contain corresponding id in repository skeleton.
3. Provide the final list of modules in the order they should be developed, based on the dependencies and logical progression of the project.

**Project Readme**:
{project_readme}

**Repository Skeleton**:
{code_framework}

**Key Components to Note**:

1. You must avoid outputting the explanation of the code, only output the json output, so I can directly use it in the next step.


**Output_example**:
{{
  "Modules": [
    {{
      "Module": "Module Core",
      "key_ids": [8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, ]
    }},
    {{
      "Module": "Factory",
      "key_ids": [6, 7]
    }},
    ...
  ]
  {{
  "development_order": [
    "Network Core",
    "Factory",
    ...
  ]
}}
"""




project_plan_using_module_generation = """
You are an expert software development planner. Your task is to analyze all dependencies in given module from a code repository. Each module is already divided by architect. Your task is to identify and outline any dependencies in repository skeleton, based on their functionality and interdependencies.

**Your Task**:
1. Analyze the functionality and interactions and include dependencies from both within the modules and other relevant parts of the repository.
2. Clearly output the dependencies in json output, Each dependency has a certain id list which contain corresponding id in repository skeleton. 
3. The task_id in json output represents the order in development.

**Project Readme**:
{project_readme}

**Repository Skeleton**:
{code_framework}

**Module to be analyzed**:
{module_to_be_analyzed}

**Output_example**:
{{
  "test" # Module Name
  : 
  [
    {{
      "task_id": 1,  
      "key_id": 4,  
      "dependency": [1, 2, 31] # key_id in repository skeleton
    }},
    {{
      "task_id": 2,  
      "key_id": 3,
      "dependency": [null]
    }},
    ... 
  ]
}}
"""



project_plan_using_module_generation_claude = """
You are an expert software development planner. Your task is to analyze all dependencies in given module from a code repository. Each module is already divided by architect. Your task is to identify and outline any dependencies in repository skeleton, based on their functionality and interdependencies.

**Your Task**:
1. Analyze the functionality and interactions and include dependencies from both within the modules and other relevant parts of the repository.
2. Clearly output the dependencies in json output, Each dependency has a certain id list which contain corresponding id in repository skeleton. 
3. The task_id in json output represents the order in development.

**Project Readme**:
{project_readme}

**Repository Skeleton**:
{code_framework}

**Module to be analyzed**:
{module_to_be_analyzed}

**Output_example**:
{{
  "test" # Module Name
  : 
  [
    {{
      "task_id": 1,  
      "key_id": 4,  
      "dependency": [1, 2, 31] # key_id in repository skeleton
    }},
    {{
      "task_id": 2,  
      "key_id": 3,
      "dependency": [null]
    }},
    ... 
  ]
}}


### Key Components to Note:

1. You must avoid outputting the explanation of the code, only output the json output, so I can directly use it in the next step.


"""


project_step_implementation_generation_base = """
You are a professional software engineer, Our task is to generate a software project based on the following overall logic:
1. Code Framework 2. Task Plan Agent 3. Code Implement 4. Error Fixing Agent 
Now you are entering the next phase of our project development, following the creation of a detailed, step-by-step development plan in the previous stage. Your current task involves systematically generating the actual code for each step outlined in the plan. 

**Project Readme**:
{project_readme}

**Code Context**:
{code_context}

**Tasks to be implemented in this step**:
{code_framework}

**Work Environment**:
{work_env}

**Rules**:
1. You should infer the specific logic rules and application methods for the code to be generated, drawing from the current step and the overall project description. This should inform your implementation, rather than simply offering a potential solution based on the framework of the functions.
2. You must avoid using 'pass' as a placeholder in your code implementation. Instead, ensure that your code thoroughly considers possible scenarios and incorporates appropriate handling logic.
3. You should follow the json format and keyword data structure in the Output Format.
4. If needed, each generated code should include necessary import statements, including third-party libraries from the work environment and local modules from the Code Context.
5. Please strictly follow the rules 1,2,3,4 strictly!


**Output Format**:
{{
  "implementation_plan": [
    {{
      "key_id": int,
      "fqn": str,
      "imports": list
      "code": str
    }},
    ...
  ]
}}


**Output Example**:
{{
  "implementation_plan": [
    {{
      "key_id": 10,
      "fqn": "textual-universal-directorytree/textual_universal_directorytree/utils.py/is_remote_path",
      "imports": [
        "from urllib.parse import urlparse",
        "from textual_universal_directorytree.main import another_function"
      ],
      "code": "def is_remote_path(path: str) -> bool:\n    if another_function(path):\n        return bool(urlparse(path).scheme)\n    return False"
    }},
    {{
      "key_id": 2,
      "fqn": "postgrestq/task_queue.py/TaskQueue/connect",
      "imports": [],
      "code": "def connect(self) -> None: ... (implementation)"
    }},
    {{
      "key_id": 4,
      "fqn": "postgrestq/task_queue.py/TaskQueue/_create_queue_table",
      "imports": [
        "import psycopg"
      ],
      "code": "def _create_queue_table(self) -> None: ... (implementation)"
    }}
  ]
}}

**Code Detials Example**:
"code": " def handle_github_url(cls, url: str | GitHubPath) -> str:
        try:
            import requests
        except ImportError as e:
            raise ImportError(
                "The requests library is required to browse GitHub files. "
                "Install `textual-universal-directorytree` with the `remote` "
                "extra to install requests."
            ) from e

        url = str(url)
        gitub_prefix = "github://"
        if gitub_prefix in url and "@" not in url:
            _, user_password = url.split("github://")
            org, repo_str = user_password.split(":")
            repo, *args = repo_str.split("/")
        elif gitub_prefix in url and "@" in url:
            return url
        else:
            msg = f"Invalid GitHub URL: {{url}}"
            raise ValueError(msg)
        token = getenv("GITHUB_TOKEN")
        auth = {{"auth": ("Bearer", token)}} if token is not None else {{}}
        resp = requests.get(
            f"https://api.github.com/repos/{{org}}/{{repo}}",
            headers={{"Accept": "application/vnd.github.v3+json"}},
            timeout=30,
            **auth,  # type: ignore[arg-type]
        )
        resp.raise_for_status()
        default_branch = resp.json()["default_branch"]
        arg_str = "/".join(args)
        github_uri = f"{{gitub_prefix}}{{org}}:{{repo}}@{{default_branch}}/{{arg_str}}".rstrip(
            "/"
        )
        return github_uri"
"""



project_step_implementation_generation_base_design = """
You are a professional software engineer, Our task is to generate a software project based on the following overall logic:
1. Code Framework 2. Task Plan Agent 3. Code Implement 4. Error Fixing Agent 
Now you are entering the next phase of our project development, following the creation of a detailed, step-by-step development plan in the previous stage. Your current task involves systematically generating the actual code for each step outlined in the plan. 

**Project Readme**:
{project_readme}

**Code Context**:
{code_context}

**Tasks to be implemented in this step**:
{code_framework}

**Work Environment**:
{work_env}

**Design Document**:
{design_info}

**Rules**:
1. You should infer the specific logic rules and application methods for the code to be generated, drawing from the current step and the overall project description. This should inform your implementation, rather than simply offering a potential solution based on the framework of the functions.
2. You must avoid using 'pass' as a placeholder in your code implementation. Instead, ensure that your code thoroughly considers possible scenarios and incorporates appropriate handling logic.
3. You should follow the json format and keyword data structure in the Output Format.
4. If needed, each generated code should include necessary import statements, including third-party libraries from the work environment and local modules from the Code Context.
5. Please strictly follow the rules 1,2,3,4 strictly!


**Output Format**:
{{
  "implementation_plan": [
    {{
      "key_id": int,
      "fqn": str,
      "imports": list
      "code": str
    }},
    ...
  ]
}}


**Output Example**:
{{
  "implementation_plan": [
    {{
      "key_id": 10,
      "fqn": "textual-universal-directorytree/textual_universal_directorytree/utils.py/is_remote_path",
      "imports": [
        "from urllib.parse import urlparse",
        "from textual_universal_directorytree.main import another_function"
      ],
      "code": "def is_remote_path(path: str) -> bool:\n    if another_function(path):\n        return bool(urlparse(path).scheme)\n    return False"
    }},
    {{
      "key_id": 2,
      "fqn": "postgrestq/task_queue.py/TaskQueue/connect",
      "imports": [],
      "code": "def connect(self) -> None: ... (implementation)"
    }},
    {{
      "key_id": 4,
      "fqn": "postgrestq/task_queue.py/TaskQueue/_create_queue_table",
      "imports": [
        "import psycopg"
      ],
      "code": "def _create_queue_table(self) -> None: ... (implementation)"
    }}
  ]
}}

**Code Detials Example**:
"code": " def handle_github_url(cls, url: str | GitHubPath) -> str:
        try:
            import requests
        except ImportError as e:
            raise ImportError(
                "The requests library is required to browse GitHub files. "
                "Install `textual-universal-directorytree` with the `remote` "
                "extra to install requests."
            ) from e

        url = str(url)
        gitub_prefix = "github://"
        if gitub_prefix in url and "@" not in url:
            _, user_password = url.split("github://")
            org, repo_str = user_password.split(":")
            repo, *args = repo_str.split("/")
        elif gitub_prefix in url and "@" in url:
            return url
        else:
            msg = f"Invalid GitHub URL: {{url}}"
            raise ValueError(msg)
        token = getenv("GITHUB_TOKEN")
        auth = {{"auth": ("Bearer", token)}} if token is not None else {{}}
        resp = requests.get(
            f"https://api.github.com/repos/{{org}}/{{repo}}",
            headers={{"Accept": "application/vnd.github.v3+json"}},
            timeout=30,
            **auth,  # type: ignore[arg-type]
        )
        resp.raise_for_status()
        default_branch = resp.json()["default_branch"]
        arg_str = "/".join(args)
        github_uri = f"{{gitub_prefix}}{{org}}:{{repo}}@{{default_branch}}/{{arg_str}}".rstrip(
            "/"
        )
        return github_uri"
"""




project_step_implementation_generation_base_claude = """
You are a professional software engineer, Our task is to generate a software project based on the following overall logic:
1. Code Framework 2. Task Plan Agent 3. Code Implement 4. Error Fixing Agent 
Now you are entering the next phase of our project development, following the creation of a detailed, step-by-step development plan in the previous stage. Your current task involves systematically generating the actual code for each step outlined in the plan. 

**Project Readme**:
{project_readme}

**Code Context**:
{code_context}

**Tasks to be implemented in this step**:
{code_framework}

**Work Environment**:
{work_env}


**Key Components to Note**:
1. You must avoid outputting the explanation of the code, only output the json output, so I can directly use it in the next step.
2. You must consider including these characters in generated code: Newlines: The \n character should be used to represent new lines within the string. Escaped Quotes: Double quotes inside the string are escaped with \\\" to ensure they are correctly interpreted within the JSON format!


**Rules**:
1. You should infer the specific logic rules and application methods for the code to be generated, drawing from the current step and the overall project description. This should inform your implementation, rather than simply offering a potential solution based on the framework of the functions.
2. You must avoid using 'pass' as a placeholder in your code implementation. Instead, ensure that your code thoroughly considers possible scenarios and incorporates appropriate handling logic.
3. You should follow the json format and keyword data structure in the Output Format.
4. If needed, each generated code should include necessary import statements, including third-party libraries from the work environment and local modules from the Code Context.
5. Please strictly follow the rules 1,2,3,4 strictly!

**Output Format**:
{{
  "implementation_plan": [
    {{
      "key_id": int,
      "fqn": str,
      "imports": list
      "code": str #You must consider including these characters in generated code: Newlines: The \n character should be used to represent new lines within the string. Escaped Quotes: Double quotes inside the string are escaped with \\\" to ensure they are correctly interpreted within the JSON output format.
    }},
    ...
  ]
}}




**Output Example**:
{{
  "implementation_plan": [
    {{
      "key_id": 10,
      "fqn": "textual-universal-directorytree/textual_universal_directorytree/utils.py/is_remote_path",
      "imports": [
        "from urllib.parse import urlparse",
        "from textual_universal_directorytree.main import another_function"
      ],
    "code": "def __init__(self, glyphset: Set[str]):\n    self.glyphset = glyphset\n    self.logger = logging.getLogger(\"ufomerge.layout\")"
    }},
    ...
  ]


**Code Detials Example**:
"code": "def handle_github_url(cls, url: str | GitHubPath) -> str:\n    try:\n        import requests\n    except ImportError as e:\n        raise ImportError(\n            \"The requests library is required to browse GitHub files. \"\n            \"Install `textual-universal-directorytree` with the `remote` \"\n            \"extra to install requests.\"\n        ) from e\n\n    url = str(url)\n    github_prefix = \"github://\"\n    if github_prefix in url and \"@\" not in url:\n        _, user_password = url.split(\"github://\")\n        org, repo_str = user_password.split(\":\")\n        repo, *args = repo_str.split(\"/\")\n    elif github_prefix in url and \"@\" in url:\n        return url\n    else:\n        msg = f\"Invalid GitHub URL: {{url}}\"\n        raise ValueError(msg)\n    token = getenv(\"GITHUB_TOKEN\")\n    auth = {{\"auth\": (\"Bearer\", token)}} if token is not None else {{}}\n    resp = requests.get(\n        f\"https://api.github.com/repos/{{org}}/{{repo}}\",\n        headers={{\"Accept\": \"application/vnd.github.v3+json\"}},\n        timeout=30,\n        **auth,  # type: ignore[arg-type]\n    )\n    resp.raise_for_status()\n    default_branch = resp.json()[\"default_branch\"]\n    arg_str = \"/\".join(args)\n    github_uri = f\"{{github_prefix}}{{org}}:{{repo}}@{{default_branch}}/{{arg_str}}\".rstrip(\n        \"/\"\n    )\n    return github_uri"
"""




project_step_implementation_generation_base_with_init = """
You are a professional software engineer, Our task is to generate a software project based on the following overall logic:
1. Code Framework 2. Task Plan Agent 3. Code Implement 4. Error Fixing Agent 
Now you are entering the next phase of our project development, following the creation of a detailed, step-by-step development plan in the previous stage. Your current task involves systematically generating the actual code for each step outlined in the plan. 

**Project Readme**:
{project_readme}

**Code Context**:
{code_context}

**Tasks to be implemented in this step**:
{code_framework}

**Work Environment**:
{work_env}

**Class Init**:
{init_context}

**Rules**:
1. You should infer the specific logic rules and application methods for the code to be generated, drawing from the current step and the overall project description. This should inform your implementation, rather than simply offering a potential solution based on the framework of the functions.
2. You must avoid using 'pass' as a placeholder in your code implementation. Instead, ensure that your code thoroughly considers possible scenarios and incorporates appropriate handling logic.
3. If the functions in tasks are not standalone, you should follow the Class Init which provides the initial setup and attributes for functions belonging to classes in the tasks.
4. You should follow the json format and keyword data structure in the Output Format.
5. If needed, each generated code should include necessary import statements, including third-party libraries from the work environment and local modules from the Code Context.
6. Please strictly follow the rules 1,2,3,4,5 strictly!


**Output Format**:
{{
  "implementation_plan": [
    {{
      "key_id": int,
      "fqn": str,
      "imports": list
      "code": str
    }},
    ...
  ]
}}


**Output Example**:
{{
  "implementation_plan": [
    {{
      "key_id": 2,
      "fqn": "textual-universal-directorytree/textual_universal_directorytree/utils.py/is_remote_path",
      "imports": [
        "from urllib.parse import urlparse",
        "from textual_universal_directorytree.main import another_function"
      ],
      "code": "def is_remote_path(path: str) -> bool:\n    if another_function(path):\n        return bool(urlparse(path).scheme)\n    return False"
    }},
    {{
      "key_id": 10,
      "fqn": "postgrestq/task_queue.py/TaskQueue/connect",
      "imports": [],
      "code": "def connect(self) -> None: ... (implementation)"
    }},
    {{
      "key_id": 3,
      "fqn": "postgrestq/task_queue.py/TaskQueue/_create_queue_table",
      "imports": [
        "import psycopg"
      ],
      "code": "def _create_queue_table(self) -> None: ... (implementation)"
    }}
  ]
}}

**Code Detials Example**:
"code": " def handle_github_url(cls, url: str | GitHubPath) -> str:
        try:
            import requests
        except ImportError as e:
            raise ImportError(
                "The requests library is required to browse GitHub files. "
                "Install `textual-universal-directorytree` with the `remote` "
                "extra to install requests."
            ) from e

        url = str(url)
        gitub_prefix = "github://"
        if gitub_prefix in url and "@" not in url:
            _, user_password = url.split("github://")
            org, repo_str = user_password.split(":")
            repo, *args = repo_str.split("/")
        elif gitub_prefix in url and "@" in url:
            return url
        else:
            msg = f"Invalid GitHub URL: {{url}}"
            raise ValueError(msg)
        token = getenv("GITHUB_TOKEN")
        auth = {{"auth": ("Bearer", token)}} if token is not None else {{}}
        resp = requests.get(
            f"https://api.github.com/repos/{{org}}/{{repo}}",
            headers={{"Accept": "application/vnd.github.v3+json"}},
            timeout=30,
            **auth,  # type: ignore[arg-type]
        )
        resp.raise_for_status()
        default_branch = resp.json()["default_branch"]
        arg_str = "/".join(args)
        github_uri = f"{{gitub_prefix}}{{org}}:{{repo}}@{{default_branch}}/{{arg_str}}".rstrip(
            "/"
        )
        return github_uri"
"""


project_step_implementation_generation_base_with_init_claude = """
You are a professional software engineer, Our task is to generate a software project based on the following overall logic:
1. Code Framework 2. Task Plan Agent 3. Code Implement 4. Error Fixing Agent 
Now you are entering the next phase of our project development, following the creation of a detailed, step-by-step development plan in the previous stage. Your current task involves systematically generating the actual code for each step outlined in the plan. 

**Project Readme**:
{project_readme}

**Code Context**:
{code_context}

**Tasks to be implemented in this step**:
{code_framework}

**Work Environment**:
{work_env}

**Class Init**:
{init_context}

**Key Components to Note**:
1. You must avoid outputting the explanation of the code, only output the json output, so I can directly use it in the next step.
2. You must consider including these characters in generated code: Newlines: The \n character should be used to represent new lines within the string. Escaped Quotes: Double quotes inside the string are escaped with \\\" to ensure they are correctly interpreted within the JSON output format.


**Rules**:
1. You should infer the specific logic rules and application methods for the code to be generated, drawing from the current step and the overall project description. This should inform your implementation, rather than simply offering a potential solution based on the framework of the functions.
2. You must avoid using 'pass' as a placeholder in your code implementation. Instead, ensure that your code thoroughly considers possible scenarios and incorporates appropriate handling logic.
3. If the functions in tasks are not standalone, you should follow the Class Init which provides the initial setup and attributes for functions belonging to classes in the tasks.
4. You should follow the json format and keyword data structure in the Output Format.
5. If needed, each generated code should include necessary import statements, including third-party libraries from the work environment and local modules from the Code Context.
6. Please strictly follow the rules 1,2,3,4,5 strictly!


**Output Format**:
{{
  "implementation_plan": [
    {{
      "key_id": int,
      "fqn": str,
      "imports": list
      "code": str #You must consider including these characters in generated code: Newlines: The \n character should be used to represent new lines within the string. Escaped Quotes: Double quotes inside the string are escaped with \\\" to ensure they are correctly interpreted within the JSON output format.
    }},
    ...
  ]
}}


**Output Example**:
{{
  "implementation_plan": [
    {{
      "key_id": 2,
      "fqn": "textual-universal-directorytree/textual_universal_directorytree/utils.py/is_remote_path",
      "imports": [
        "from urllib.parse import urlparse",
        "from textual_universal_directorytree.main import another_function"
      ],
    "code": "def __init__(self, glyphset: Set[str]):\n    self.glyphset = glyphset\n    self.logger = logging.getLogger(\"ufomerge.layout\")"    
    }},
    ....
  ]
}}

**Code Detials Example**:
"code": "def handle_github_url(cls, url: str | GitHubPath) -> str:\n    try:\n        import requests\n    except ImportError as e:\n        raise ImportError(\n            \"The requests library is required to browse GitHub files. \"\n            \"Install `textual-universal-directorytree` with the `remote` \"\n            \"extra to install requests.\"\n        ) from e\n\n    url = str(url)\n    github_prefix = \"github://\"\n    if github_prefix in url and \"@\" not in url:\n        _, user_password = url.split(\"github://\")\n        org, repo_str = user_password.split(\":\")\n        repo, *args = repo_str.split(\"/\")\n    elif github_prefix in url and \"@\" in url:\n        return url\n    else:\n        msg = f\"Invalid GitHub URL: {{url}}\"\n        raise ValueError(msg)\n    token = getenv(\"GITHUB_TOKEN\")\n    auth = {{\"auth\": (\"Bearer\", token)}} if token is not None else {{}}\n    resp = requests.get(\n        f\"https://api.github.com/repos/{{org}}/{{repo}}\",\n        headers={{\"Accept\": \"application/vnd.github.v3+json\"}},\n        timeout=30,\n        **auth,  # type: ignore[arg-type]\n    )\n    resp.raise_for_status()\n    default_branch = resp.json()[\"default_branch\"]\n    arg_str = \"/\".join(args)\n    github_uri = f\"{{github_prefix}}{{org}}:{{repo}}@{{default_branch}}/{{arg_str}}\".rstrip(\n        \"/\"\n    )\n    return github_uri"
"""





project_step_implementation_generation_base_with_init_design = """
You are a professional software engineer, Our task is to generate a software project based on the following overall logic:
1. Code Framework 2. Task Plan Agent 3. Code Implement 4. Error Fixing Agent 
Now you are entering the next phase of our project development, following the creation of a detailed, step-by-step development plan in the previous stage. Your current task involves systematically generating the actual code for each step outlined in the plan. 

**Project Readme**:
{project_readme}

**Design Document**:
{design_info}

**Code Context**:
{code_context}

**Tasks to be implemented in this step**:
{code_framework}

**Work Environment**:
{work_env}

**Class Init**:
{init_context}

**Rules**:
1. You should infer the specific logic rules and application methods for the code to be generated, drawing from the current step and the overall project description. This should inform your implementation, rather than simply offering a potential solution based on the framework of the functions.
2. You must avoid using 'pass' as a placeholder in your code implementation. Instead, ensure that your code thoroughly considers possible scenarios and incorporates appropriate handling logic.
3. If the functions in tasks are not standalone, you should follow the Class Init which provides the initial setup and attributes for functions belonging to classes in the tasks.
4. You should follow the json format and keyword data structure in the Output Format.
5. If needed, each generated code should include necessary import statements, including third-party libraries from the work environment and local modules from the Code Context.
6. Please strictly follow the rules 1,2,3,4,5 strictly!


**Output Format**:
{{
  "implementation_plan": [
    {{
      "key_id": int,
      "fqn": str,
      "imports": list
      "code": str
    }},
    ...
  ]
}}


**Output Example**:
{{
  "implementation_plan": [
    {{
      "key_id": 2,
      "fqn": "textual-universal-directorytree/textual_universal_directorytree/utils.py/is_remote_path",
      "imports": [
        "from urllib.parse import urlparse",
        "from textual_universal_directorytree.main import another_function"
      ],
      "code": "def is_remote_path(path: str) -> bool:\n    if another_function(path):\n        return bool(urlparse(path).scheme)\n    return False"
    }},
    {{
      "key_id": 10,
      "fqn": "postgrestq/task_queue.py/TaskQueue/connect",
      "imports": [],
      "code": "def connect(self) -> None: ... (implementation)"
    }},
    {{
      "key_id": 3,
      "fqn": "postgrestq/task_queue.py/TaskQueue/_create_queue_table",
      "imports": [
        "import psycopg"
      ],
      "code": "def _create_queue_table(self) -> None: ... (implementation)"
    }}
  ]
}}

**Code Detials Example**:
"code": " def handle_github_url(cls, url: str | GitHubPath) -> str:
        try:
            import requests
        except ImportError as e:
            raise ImportError(
                "The requests library is required to browse GitHub files. "
                "Install `textual-universal-directorytree` with the `remote` "
                "extra to install requests."
            ) from e

        url = str(url)
        gitub_prefix = "github://"
        if gitub_prefix in url and "@" not in url:
            _, user_password = url.split("github://")
            org, repo_str = user_password.split(":")
            repo, *args = repo_str.split("/")
        elif gitub_prefix in url and "@" in url:
            return url
        else:
            msg = f"Invalid GitHub URL: {{url}}"
            raise ValueError(msg)
        token = getenv("GITHUB_TOKEN")
        auth = {{"auth": ("Bearer", token)}} if token is not None else {{}}
        resp = requests.get(
            f"https://api.github.com/repos/{{org}}/{{repo}}",
            headers={{"Accept": "application/vnd.github.v3+json"}},
            timeout=30,
            **auth,  # type: ignore[arg-type]
        )
        resp.raise_for_status()
        default_branch = resp.json()["default_branch"]
        arg_str = "/".join(args)
        github_uri = f"{{gitub_prefix}}{{org}}:{{repo}}@{{default_branch}}/{{arg_str}}".rstrip(
            "/"
        )
        return github_uri"
"""



project_step_implementation_generation = """
As a professional software engineer, you are entering the next phase of our project development, following the creation of a detailed, step-by-step development plan in the previous stage. Your current task involves systematically generating the actual code for each step outlined in the plan. This process requires you to focus on one step at a time.

**Project Readme**:
{project_readme}

**Code to be implemented in this step**:
{code_framework}

**Task Reference**: 
{reference}

**Code Requirements**:
{comment}

**Third Party Libraries**:
{third_party_libraries}

**Class Attributes**:
{class_attribute}

**rules**:
1. You should infer the specific logic rules and application methods for the code to be generated, drawing from the current step and the overall project description. This should inform your implementation, rather than simply offering a potential solution based on the framework of the functions. You must avoid using 'pass' as a placeholder in your code implementation.
2. 
3. You are permitted to utilize third-party libraries as needed, and you may also reference other classes or functions that have been outlined in the development plan steps.
4. You should focus on implementing the function's code based on information such as Code Requirements, Third Party Libraries, etc., rather than expanding on the class's potential initializations and attributes.
5. You should follow the json format and keyword data structure in the Output_example. If methods in one task exist, separate the methods to different tasks.
6. Please strictly follow the rules 1,2,3,4,5 strictly!


**Output Format**:
{{
  "implementation_plan": [
    {{
      "step": int,
      "description": source_code_comment,
      "tasks": [ # every task should be a dict and represent a method
        {{
          "file": str,
          "class": str,
          "method": str,
          "implementation_details": {{
          "Code": "xxx" # code implementation, avoid pass and implement the logic
          }}
        }},
        ....
      ]
    }},
  ],
  "third_party_libraries": ["xxx"], # third-party libraries used in the implementation
}}


**Output Example**:
{{
  "implementation_plan": [
    {{
      "step": 1,
      "description": "Implement initialization logic for GitHubAccessor.",
      "tasks": [ 
        {{
          "file": "alternate_paths.py",
          "class": "_GitHubAccessor",
          "method": "_GitHubAccessor.__init__",
          "implementation_details": {{
          "Code": "xxx" # code implementation, avoid pass and implement the logic
          }}
        }},
        {{
          "file": "alternate_paths.py",
          "class": "_GitHubAccessor",
          "method": "_GitHubAccessor.xxx",
          "implementation_details": {{
          "Code": "xxx" # code implementation, avoid pass and implement the logic
          }}
        }},
        ....
      ]
    }},
  ],
  "third_party_libraries": ["xxx"], # third-party libraries used in the implementation
}}

***Code_detials_example***:
"Code_detial": " def handle_github_url(cls, url: str | GitHubPath) -> str:
        try:
            import requests
        except ImportError as e:
            raise ImportError(
                "The requests library is required to browse GitHub files. "
                "Install `textual-universal-directorytree` with the `remote` "
                "extra to install requests."
            ) from e

        url = str(url)
        gitub_prefix = "github://"
        if gitub_prefix in url and "@" not in url:
            _, user_password = url.split("github://")
            org, repo_str = user_password.split(":")
            repo, *args = repo_str.split("/")
        elif gitub_prefix in url and "@" in url:
            return url
        else:
            msg = f"Invalid GitHub URL: {{url}}"
            raise ValueError(msg)
        token = getenv("GITHUB_TOKEN")
        auth = {{"auth": ("Bearer", token)}} if token is not None else {{}}
        resp = requests.get(
            f"https://api.github.com/repos/{{org}}/{{repo}}",
            headers={{"Accept": "application/vnd.github.v3+json"}},
            timeout=30,
            **auth,  # type: ignore[arg-type]
        )
        resp.raise_for_status()
        default_branch = resp.json()["default_branch"]
        arg_str = "/".join(args)
        github_uri = f"{{gitub_prefix}}{{org}}:{{repo}}@{{default_branch}}/{{arg_str}}".rstrip(
            "/"
        )
        return github_uri"
"""













project_step_implementation_generation_pass = """
As a professional software engineer, you are entering the next phase of our project development, adding details to the code that we didn't get to implement in the previous step of the code implementation. Your current task is to make a further additional implementation of the function that generated the pass placeholder in the previous step, in which you need to understand why the code part was not implemented previously, based on possible project information, and finally give a new implementation of the code.

**Project Readme**:
{project_readme}

**Code Context in Implementation Step**:
{generated_context}

**Code to be implemented**:
{code_framework}

**Task Reference**: 
{reference}

**Code Requirements**:
{comment}

**Third Party Libraries**:
{third_party_libraries}

**Class Attributes**:
{class_attribute}

**rules**:
1. You should infer the specific logic rules and application methods for the code to be generated, drawing from the current step and the overall project description. This should inform your implementation, rather than simply offering a potential solution based on the framework of the functions.
2. You must avoid using 'pass' as a placeholder in your code implementation. Instead, ensure that your code thoroughly considers possible scenarios and incorporates appropriate handling logic!
3. You should focus on implementing the function's code based on information such as Code Requirements, Third Party Libraries, etc., rather than expanding on the class's potential initializations and attributes.
4. You should follow the json format and keyword data structure in the Output Format. If methods in one task exist, separate the methods to different tasks.
5. Please strictly follow the rules 1,2,3,4 strictly!

**Output Format**:
{{
"code": code_new_version
}}

***Code_detials_example***:
{{
"code": " def handle_github_url(cls, url: str | GitHubPath) -> str:
        try:
            import requests
        except ImportError as e:
            raise ImportError(
                "The requests library is required to browse GitHub files. "
                "Install `textual-universal-directorytree` with the `remote` "
                "extra to install requests."
            ) from e

        url = str(url)
        gitub_prefix = "github://"
        if gitub_prefix in url and "@" not in url:
            _, user_password = url.split("github://")
            org, repo_str = user_password.split(":")
            repo, *args = repo_str.split("/")
        elif gitub_prefix in url and "@" in url:
            return url
        else:
            msg = f"Invalid GitHub URL: {{url}}"
            raise ValueError(msg)
        token = getenv("GITHUB_TOKEN")
        auth = {{"auth": ("Bearer", token)}} if token is not None else {{}}
        resp = requests.get(
            f"https://api.github.com/repos/{{org}}/{{repo}}",
            headers={{"Accept": "application/vnd.github.v3+json"}},
            timeout=30,
            **auth,  # type: ignore[arg-type]
        )
        resp.raise_for_status()
        default_branch = resp.json()["default_branch"]
        arg_str = "/".join(args)
        github_uri = f"{{gitub_prefix}}{{org}}:{{repo}}@{{default_branch}}/{{arg_str}}".rstrip(
            "/"
        )
        return github_uri"
"""



fixed_prompt = """
You are a professional software engineer, Our task is to generate a software project based on the following overall logic:
1. Code Framework 2. Task Plan Agent 3. Code Implement 4. Error Fixing Agent. 
We will implement the corresponding code according to this logic. At this step, your current task involves fixing the syntax error in generated code and conclude the reason of the error conclusion so that we can use code to replace the code signature.

**Code to be Fixed in This Step**:
{code_to_be_fixed}

**Error Description**:
{error_description}

**Rules**:
1. You should give the new version of the code with the error fixed.
2. Please avoid changing the function signature, only focus on fixing the error in the code!
3. You should follow the json format and keyword data structure in the Output Format.
4. Please strictly follow the rules 1,2,3 strictly!

**Output Example**:
{{
    "new_version_code": "def add_word(self, word: str) -> int:\\n    try:\\n        # Implement logic to add a word to the guessed list\\n        pass  # Placeholder for actual implementation\\n    except Exception as e:\\n        print(\\"An error occurred\\")  # Basic exception handling\\n        pass",
    "error_conclusion": {{
        "type": "SyntaxError",
        "message": "Missing implementation for the add_word function",
        "line": 3
    }}
}}
"""



fixed_prompt_claude = """
You are a professional software engineer, Our task is to generate a software project based on the following overall logic:
1. Code Framework 2. Task Plan Agent 3. Code Implement 4. Error Fixing Agent. 
We will implement the corresponding code according to this logic. At this step, your current task involves fixing the syntax error in generated code and conclude the reason of the error conclusion so that we can use code to replace the code signature.

**Code to be Fixed in This Step**:
{code_to_be_fixed}

**Error Description**:
{error_description}

**Rules**:
1. You should give the new version of the code with the error fixed.
2. Please avoid changing the function signature, only focus on fixing the error in the code!
3. You should follow the json format and keyword data structure in the Output Format.
4. Please strictly follow the rules 1,2,3 strictly!

**Output Example**:
{{
    "new_version_code": "def add_word(self, word: str) -> int:\\n    try:\\n        # Implement logic to add a word to the guessed list\\n        pass  # Placeholder for actual implementation\\n    except Exception as e:\\n        print(\\"An error occurred\\")  # Basic exception handling\\n        pass",
    "error_conclusion": {{
        "type": "SyntaxError",
        "message": "Missing implementation for the add_word function",
        "line": 3
    }}
}}
### Key Components to Note:
1. You must avoid outputting the explanation of the code, only output the json output, so I can directly use it in the next step.

"""




# from typing import Callable, Any, Coroutine
# def handler_translator(self, message: str, source_lang: str) -> Callable[[Callable[..., object]], Callable[[Any, Any, str], Coroutine[Any, Any, Any]]:
#     def decorator(func: Callable[..., object]) -> Callable[[Any, Any, str], Coroutine[Any, Any, Any]]:
#         async def wrapper(update: Any, context: Any, message: str) -> None:
#             # Translation logic based on source_lang
#             translated_message = self.translator_service.translate(message, source_lang)
#             await func(update, context, translated_message)
#         return wrapper
#     return decorator

# **Input_example**:
# "def new_game(self, size: int, cubefile: str, dict: BoggleDictionary) -> None:\n    try:\n        # Implement logic to create a new Boggle game\n    except OSError as e:\n        raise OSError('The cubefile cannot be opened or read.') from e"
# **Output_example**:
# {{
# "code": "def new_game(self, size: int, cubefile: str, dict: BoggleDictionary) -> None:\n    try:\n        # Implement logic to create a new Boggle game\\n        pass    except OSError as e:\n        raise OSError('The cubefile cannot be opened or read.') from e"
# }}



# def get_updated_expired_task(self, task_id: UUID) -> Tuple[Optional[str], Optional[int]]:
#     try:
#         with self._conn.cursor() as cur:
#             cur.execute(
#                 'UPDATE task_queue SET processing = false, deadline = current_timestamp + CAST(lease_timeout || ' seconds' AS INTERVAL), ttl = ttl - 1 WHERE id = %s RETURNING task, ttl',
#                 (task_id,)
#             )
#             result = cur.fetchone()
#             if result:
#                 task, ttl = result
#                 return task, ttl
#             else:
#                 return None, None
#     except Exception as e:
#         self.logger.error(f'Error updating expired task: {e}')
#         return None, None
    

# def get_updated_expired_task(self, task_id: UUID) -> Tuple[Optional[str], Optional[int]]:
#     try:
#         with self._conn.cursor() as cur:
#             cur.execute(
#                 'UPDATE task_queue SET processing = false, deadline = current_timestamp + CAST(lease_timeout || \' seconds\' AS INTERVAL), ttl = ttl - 1 WHERE id = %s RETURNING task, ttl',
#                 (task_id,)
#             )
#             result = cur.fetchone()
#             if result:
#                 task, ttl = result
#                 return task, ttl
#             else:
#                 return None, None
#     except Exception as e:
#         self.logger.error(f'Error updating expired task: {e}')
#         return None, None



