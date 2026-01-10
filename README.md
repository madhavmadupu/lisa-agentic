# LISA (Local Intelligence Software Architect)

**An Autonomous Multi-Agent System for Secure, Air-Gapped Code Generation & Review**

LISA is a local-first agentic framework designed to automate the Software Development Lifecycle (SDLC). By leveraging **Ollama** for local inference, LISA allows developers to generate, test, and refactor code without ever sending sensitive IP to the cloud.

## Getting Started

1.  **Prerequisites**:
    *   [Ollama](https://ollama.com/) installed.
    *   Python 3.10+ installed.

2.  **Setup**:
    ```bash
    # Install dependencies
    pip install -r requirements.txt
    
    # Pull required models
    chmod +x ollama_config.sh
    ./ollama_config.sh
    ```

3.  **Running**:
    ```bash
    streamlit run app.py
    ```

## Architecture

*   **Architect**: Plans the execution.
*   **Coder**: Implements the code.
*   **Reviewer**: Validates and tests the code.

## License
MIT
