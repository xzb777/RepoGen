# RepoGen: Exploring Repository Generation with Large Language Models

This repository contains the technical details supporting the paper *"RepoGen: Exploring Repository Generation with Large Language Models."* RepoGen aims to streamline the process of repository generation through code automation techniques, leveraging advanced language models.

## Contents
- [Introduction](#introduction)
- [How to Use](#how-to-use)
  - [Setup](#setup)
  - [Inference](#inference)
  - [Evaluation](#evaluation)
  - [New Version](#next-version)

## Introduction
This project serves as the implementation basis for our paper, containing various modules for data mining, environment configuration, and the core inference logic.

### Directory Structure:
- **`cleaned_repo`**: Contains the repositories used in our benchmark.
- **`datamining`**: Scripts and metrics for project scraping, as detailed in the paper.
- **`env`**: Environment settings for the repository generation process.
- **`repogen`**: Core code responsible for inference and evaluation.
- **`results`**: Stores outputs from both plan agents and code agents.
- **`tools`**: Utility scripts and additional tools supporting the project.

## How to Use
### Setup
We use two environment setup options: using Docker and Conda. Detailed Docker environment setup will be released soon. For Conda, check the `env` directory for configuration files.

To gather meta information from your project repository, run the following command:

```bash
python repogen/get_meta_info.py /path/to/repo /path/to/output
```
This command will extract function-based metadata from the given repository and save it to the output path. We will also provide preprocessed meta-analysis results and additional scripts in future releases. Dependency extraction will be uploaded in upcoming versions.


### Inference
Before running the repository generation, set up your environment variables:

```bash
export OPENAI_API_KEY="your_api_key"
export OPENAI_API_Base="your_base_url"
```

Next, to initiate code generation, adjust the parameters in `repoGen.py` according to your use case. Example:

```python
python repoGen.py --repo_dataset "repogen/data" --result_dir "repogen/results" --plan_gen --code_gen
```

You can configure additional settings such as:

- **`--plan_gen`**: To generate plans.
- **`--code_gen`**: To generate code.
- **`--valid_gen`**: To validate generated code.

#### Advanced Configuration

Additionally, you can further customize the process by setting specific parameters for different strategies, models, and ablation studies.

- **Strategy Configuration**:  
  You can choose different strategies for repository processing. These strategies influence how the repository and code are generated. For example:

  - **`--current_strategy`**:  
    Available strategies:
    - `base_10`
    - `base_20`
    - `base_comment`
    - `base_dep`
    - `base_design`
    - `base_import`
    - `metagpt`
    - `chatdev`

- **Model Selection**:  
  You can choose the model to use for code generation:

  - **`--selected_model`**: (default: `'LLMUtil.GPT4_0125_PREVIEW_MODEL_NAME'`)  
    Available models:
    - `LLMUtil.GPT4_0125_PREVIEW_MODEL_NAME`
    - `LLMUtil.GPT3_5_TURBO_0125_MODEL_NAME`
    - `LLMUtil.Claude3_5_MODEL_NAME`
    - `chatdev`
    - `metagpt`




### Evaluation
You can run tests by setting up the `config` files and executing the following:

```bash
python test_get.py --config "path_to_config"
```

### Next Version
In upcoming versions, we will provide more streamlined scripts, comprehensive preprocessed data to further enhance ease of use. Additionally, we will release the complete working environment from our experiments, along with the scripts used for data scraping and processing.

