# LISA (Local Intelligence Software Architect)

**An Autonomous Multi-Agent System for Secure, Air-Gapped Code Generation & Review**

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.10+-blue.svg)
![Status](https://img.shields.io/badge/status-active-success.svg)

---

## 1. Executive Summary

In 2026, data privacy is the primary hurdle for enterprise AI adoption. **LISA** is a production-ready, local-first agentic framework designed to automate the Software Development Lifecycle (SDLC). By leveraging **Ollama** for local inference, LISA allows developers to generate, test, and refactor code without ever sending sensitive IP to the cloud. It utilizes a "Self-Correction Loop" where specialized agents critique and fix code autonomously.

## 2. Problem Statement

Cloud-based AI (GitHub Copilot, GPT-4) poses security risks for proprietary codebases. Furthermore, single-prompt AI generation often leads to "hallucinated" code that fails to run. Developers need a system that:
1.  **Stays Local:** Runs 100% offline.
2.  **Self-Heals:** Tests its own code and fixes errors before presenting them to the user.
3.  **Specializes:** Uses different models for different tasks (e.g., Coding vs. Reasoning).

## 3. Documentation

*   [**System Architecture & Tech Stack**](docs/architecture.md): Deep dive into the agents, orchestration, and engineering features.
*   [**Implementation Roadmap**](docs/roadmap.md): Phased plan for development and future enhancements.
*   [**Showcase & Demos**](docs/demo_guide.md): Guide for demonstrating LISA's capabilities.

## 4. Project Structure

```text
├── agents/            # Agent definitions (Architect, Coder, Reviewer)
├── docs/              # Detailed documentation
│   ├── architecture.md
│   ├── roadmap.md
│   └── demo_guide.md
├── state/             # LangGraph state management
├── tests/             # Unit and integration tests
├── tools/             # Utilities and tools for agents
├── workspace/         # Temporary workspace for code generation
├── app.py             # Main application entry point (Streamlit)
├── ollama_config.sh   # Configuration script for Ollama models
├── requirements.txt   # Python dependencies
└── README.md          # Project documentation
```

## 🏗️ System Architecture
LISA utilizes a stateful multi-agent orchestration pattern built on LangGraph.
<img width="4642" height="2910" alt="image" src="https://github.com/user-attachments/assets/4b148e69-69ac-4509-b9eb-41d6f83d3b48" />


## 5. Getting Started

### Prerequisites
*   [Ollama](https://ollama.com/) installed and running.
*   Python 3.10 or higher installed.

### Setup

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/madhavmadupu/lisa-agentic.git
    cd lisa-agentic
    ```

2.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Configure Models:**
    Ensure you have the required Ollama models pulled. You can use the provided script:
    ```bash
    chmod +x ollama_config.sh
    ./ollama_config.sh
    ```

### Running the Application

Launch the Streamlit dashboard:
```bash
streamlit run app.py
```

## 6. Contributing

We welcome contributions to LISA! Please follow these guidelines to ensure a smooth collaboration process.

### Code Organization
*   Keep functions small and focused.
*   Use descriptive variable and function names.
*   Comment complex logic explanations.

### Pull Requests
1.  Fork the repository and create your branch from `main`.
2.  If you've added code that should be tested, add tests.
3.  Ensure the test suite passes.
4.  Make sure your code lints.
5.  Issue that the pull request solves should be referenced in the PR description.

### Issues
*   Use the issue tracker to report bugs or request features.
*   Be clear and descriptive in your bug reports. Include reproduction steps.

## 7. License

This project is licensed under the MIT License - see the LICENSE file for details.
