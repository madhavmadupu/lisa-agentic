# Setup Guide

## Prerequisites

Before running LISA, ensure you have the following installed on your system:

-   **Python 3.10+**: [Download Python](https://www.python.org/downloads/)
-   **Ollama**: [Download Ollama](https://ollama.com/)

## Installation

1.  **Clone the Repository** (if applicable) or navigate to the project directory:
    ```bash
    cd lisa-agentic
    ```

2.  **Create a Virtual Environment**:
    It is recommended to use a virtual environment to manage dependencies.
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```

3.  **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

## Model Configuration

LISA relies on three specific local LLMs running via Ollama. You need to pull these models before running the application.

1.  **Make the config script executable** (Linux/Mac):
    ```bash
    chmod +x ollama_config.sh
    ```

2.  **Run the script to pull models**:
    ```bash
    ./ollama_config.sh
    ```

    **Or manually pull the models:**
    ```bash
    ollama pull llama3.1:8b
    ollama pull qwen2.5-coder:7b
    ollama pull mistral-nemo
    ```

    *   **Architect Model**: `llama3.1:8b`
    *   **Coder Model**: `qwen2.5-coder:7b`
    *   **Reviewer Model**: `mistral-nemo`

    > **Note:** Ensure your machine has enough RAM/VRAM to run these models. 16GB+ RAM is recommended.

## Running the Application

Once everything is set up, you can launch the LISA dashboard:

```bash
streamlit run app.py
```

This will open the application in your default web browser (usually at `http://localhost:8501`).
