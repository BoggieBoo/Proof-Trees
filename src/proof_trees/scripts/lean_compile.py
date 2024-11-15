import os
import subprocess

def lean_compile(state: str):
    # Get the current working directory (where your Lake project is)
    project_dir = os.getcwd()
    temp_file_path = os.path.join(project_dir, "hello_world.lean")
    
    with open(temp_file_path, "w") as f:
        f.write(state)
    
    # First make sure we're in the Lake project directory
    os.chdir(project_dir)
    
    # Try using lake env to run lean
    result = subprocess.run(
        ['lake', 'env', 'lean', temp_file_path],
        capture_output=True,
        text=True
    )
    
    if result.returncode == 0:
        return False
    else:
        return result.stdout