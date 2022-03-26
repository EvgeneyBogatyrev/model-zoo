import os
import stat
import shutil
import subprocess
from pathlib import Path

# EXAMPLE CODE

def rmtree(top):
    # Remove files recursively, changing their permission
    for root, dirs, files in os.walk(top, topdown=False):
        for name in files:
            filename = os.path.join(root, name)
            os.chmod(filename, stat.S_IWUSR)
            os.remove(filename)
        for name in dirs:
            os.rmdir(os.path.join(root, name))
    os.rmdir(top)


def clone_repository(model_name, path_to_clone, overwrite_model=False, silent=True):
    # TODO: Check if model exists
    
    REPOSITORY_URL = "https://github.com/EvgeneyZ/model-zoo"

    # If directory with model name already exists:
    model_path = path_to_clone.joinpath(model_name)
    if Path.is_dir(model_path):
        if overwrite_model:
            rmtree(model_path)
        else:
            return

    # Remove model-zoo directory if it exists
    model_zoo_path = path_to_clone.joinpath("model-zoo")
    if Path.is_dir(model_zoo_path):
        rmtree(model_zoo_path)

    # Clone the repository
    subprocess.run(["git", "clone", REPOSITORY_URL, model_zoo_path], capture_output=silent)
    
    # Init submodules
    subprocess.run(["git", "submodule", "init"], cwd=model_zoo_path, capture_output=silent)
    
    # Clone submodule with desired model
    subprocess.run(["git", "submodule", "update", "--remote", model_name], cwd=model_zoo_path, capture_output=silent)
    
    # Move the model outside the repository
    shutil.move(Path.joinpath(model_zoo_path, model_name), Path.joinpath(path_to_clone, model_name))
    
    # Remove the repository
    rmtree(model_zoo_path)