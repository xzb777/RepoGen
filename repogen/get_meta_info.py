import sys
import json
from pathlib import Path
from tools.preprocess import FunctionBaseConstruction

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python get_meta_info.py <repo_path> <output_path>")
    else:
        repo_path = sys.argv[1]
        output_path = sys.argv[2]
        functinbase = FunctionBaseConstruction()
        dataset = functinbase.extract_function_base(directory=repo_path)
        with open(output_path, 'w') as f:
            json.dump(dataset, f)
