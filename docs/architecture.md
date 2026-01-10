# System Architecture & Engineering Features

## System Architecture

LISA uses a **Graph-based Orchestration** (via LangGraph) to manage three distinct agents:

### **A. The Architect (Llama 3.1 - 8B)**
*   **Role:** Analyzes the user's natural language request.
*   **Function:** Breaks the request into a technical "Execution Plan" (JSON format).

### **B. The Coder (Qwen2.5-Coder - 7B)**
*   **Role:** Implements the logic based on the Architect's plan.
*   **Function:** Writes Python/JS code and saves it to a temporary local workspace.

### **C. The Reviewer (Mistral-Small)**
*   **Role:** The "Quality Gate."
*   **Function:** 
    *   **Static Analysis:** Runs local linters (PyLint/Flake8).
    *   **Dynamic Analysis:** Executes the code in a restricted subprocess to see if it passes.
    *   **Feedback Loop:** If the code fails, the Reviewer sends the error logs back to the **Coder** for a "Retry." (Max 3 attempts).

---

## Tech Stack (2026 Standards)
*   **Inference Engine:** [Ollama API](https://ollama.com/) (Managing local model lifecycle).
*   **Models:** `qwen2.5-coder:7b`, `llama3.1:8b`, `mistral-nemo`.
*   **Orchestration:** LangGraph (for stateful, cyclical agent logic).
*   **Memory/Context:** ChromaDB (Vector store for local documentation RAG).
*   **Environment:** Docker (to sandbox the code execution for the Reviewer agent).
*   **Frontend:** Streamlit or Chainlit for the engineer’s dashboard.

---

## Key Engineering Features

### **1. Agentic Self-Correction**
Unlike standard RAG, LISA implements a **reflexion pattern**. If the code execution fails, the system captures the `Traceback` and automatically feeds it back into the LLM as a new prompt to fix the bug.

### **2. Hybrid RAG Pipeline**
The system indexes the local project directory. When a task is assigned, the **Architect** queries the local Vector DB to understand existing project patterns before suggesting new code.

### **3. Performance Monitoring (AI Observability)**
LISA tracks:
*   **Token Throughput:** Measured via Ollama’s `/api/generate` response headers.
*   **Success Rate:** Percentage of tasks solved without human intervention.
*   **Inference Latency:** Monitoring the overhead of running multiple local models.
