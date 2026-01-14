import os

class Config:
    # Infrastructure
    WORKSPACE_DIR = os.getenv("LISA_WORKSPACE", os.path.abspath("workspace"))
    OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://127.0.0.1:11434")
    
    # Models
    ARCHITECT_MODEL = os.getenv("ARCHITECT_MODEL", "llama3.1:8b")
    CODER_MODEL = os.getenv("CODER_MODEL", "qwen2.5-coder:7b")
    REVIEWER_MODEL = os.getenv("REVIEWER_MODEL", "mistral-nemo")

    # App Settings
    DATABASE_PATH = os.getenv("DATABASE_PATH", "lisa.db")
    DEBUG_LOG_PATH = os.getenv("DEBUG_LOG_PATH", "backend_debug.log")

config = Config()
