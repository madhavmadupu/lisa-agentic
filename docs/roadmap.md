# Implementation Roadmap

### **Phase 1: Inference Setup**
*   Configure Ollama with optimized quantization (GGUF/4-bit) to ensure three models can reside in VRAM simultaneously (or swap efficiently).

### **Phase 2: Graph Development**
*   Define the nodes (Agents) and edges (Transitions) in LangGraph.
*   Implement the "Conditional Edge" that determines if code should go to the user or back to the coder for fixing.

### **Phase 3: Tool Integration**
*   Create Python functions that the agents can call to read/write files and execute shell commands.

### **Phase 4: Evaluation**
*   Run a benchmark using the **HumanEval** dataset locally to measure the system's accuracy improvements compared to a single-prompt LLM.
