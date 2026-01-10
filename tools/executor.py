import subprocess
import os
import sys

# Define workspace
WORKSPACE_DIR = os.path.abspath("workspace")

def execute_python(filename: str) -> dict:
    """
    Executes a Python script located in the workspace.
    
    Args:
        filename (str): The script filename.
        
    Returns:
        dict: stdout, stderr, and return_code.
    """
    safe_path = os.path.abspath(os.path.join(WORKSPACE_DIR, filename))
    
    # Security check
    if not safe_path.startswith(WORKSPACE_DIR):
        return {"error": "Access denied", "stdout": "", "stderr": "Cannot execute outside workspace."}
    
    if not os.path.exists(safe_path):
        return {"error": "File not found", "stdout": "", "stderr": f"File {filename} does not exist."}

    try:
        # executing with the same python interpreter
        result = subprocess.run(
            [sys.executable, safe_path],
            capture_output=True,
            text=True,
            timeout=30, # 30 seconds timeout
            cwd=WORKSPACE_DIR # Set working directory to workspace
        )
        return {
            "return_code": result.returncode,
            "stdout": result.stdout,
            "stderr": result.stderr
        }
    except subprocess.TimeoutExpired:
        return {
            "return_code": -1,
            "stdout": "",
            "stderr": "Execution timed out (30s limit)."
        }
    except Exception as e:
        return {
            "return_code": -1,
            "stdout": "",
            "stderr": f"System execution error: {str(e)}"
        }
