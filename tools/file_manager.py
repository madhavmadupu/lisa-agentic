import os
from typing import List, Dict, Union

# Define the workspace directory where agents are allowed to write
WORKSPACE_DIR = os.path.abspath("workspace")

def ensure_workspace():
    """Ensure the workspace directory exists."""
    if not os.path.exists(WORKSPACE_DIR):
        os.makedirs(WORKSPACE_DIR)

def write_file(filename: str, content: str) -> str:
    """
    Writes content to a file in the workspace.
    
    Args:
        filename (str): The name of the file (relative to workspace).
        content (str): The content to write.
        
    Returns:
        str: Success message or error.
    """
    ensure_workspace()
    
    # Prevent directory traversal
    safe_path = os.path.abspath(os.path.join(WORKSPACE_DIR, filename))
    if not safe_path.startswith(WORKSPACE_DIR):
        return f"Error: Access denied. Cannot write outside workspace: {filename}"
        
    try:
        with open(safe_path, "w", encoding="utf-8") as f:
            f.write(content)
        return f"Successfully wrote to {filename}"
    except Exception as e:
        return f"Error writing file: {str(e)}"

def read_file(filename: str) -> str:
    """
    Reads content from a file in the workspace.
    
    Args:
        filename (str): The name of the file.
        
    Returns:
        str: File content or error.
    """
    ensure_workspace()
    
    safe_path = os.path.abspath(os.path.join(WORKSPACE_DIR, filename))
    if not safe_path.startswith(WORKSPACE_DIR):
        return f"Error: Access denied. Cannot read outside workspace: {filename}"
        
    if not os.path.exists(safe_path):
        return f"Error: File not found: {filename}"
        
    try:
        with open(safe_path, "r", encoding="utf-8") as f:
            return f.read()
    except Exception as e:
        return f"Error reading file: {str(e)}"

def list_files() -> List[str]:
    """Lists all files in the workspace."""
    ensure_workspace()
    return os.listdir(WORKSPACE_DIR)

def clear_workspace() -> str:
    """Deletes all files in the workspace."""
    ensure_workspace()
    try:
        files = os.listdir(WORKSPACE_DIR)
        for file in files:
            file_path = os.path.join(WORKSPACE_DIR, file)
            if os.path.isfile(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                import shutil
                shutil.rmtree(file_path)
        return "Workspace cleared successfully."
    except Exception as e:
        return f"Error clearing workspace: {str(e)}"
