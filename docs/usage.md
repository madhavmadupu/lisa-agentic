# Usage Guide

This guide describes how to use the LISA dashboard to generate and review code.

## Starting the Dashboard

Ensure you have followed the [Setup Guide](setup.md) and have the necessary models pulled.

Run the application:
```bash
streamlit run app.py
```

## The Workflow

### 1. Enter Your Request
On the main dashboard, you will see a text input area. Enter a clear, descriptive request for the software you want to build.

**Example Requests:**
*   "Create a Python script that scrapes the top 10 headlines from Hacker News and saves them to a CSV file."
*   "Write a calculator class with add, subtract, multiply, and divide methods, including error handling for division by zero."
*   "Build a simple REST API using Flask for a Todo application."

### 2. Monitoring Progress
Once you submit the request, LISA's agents will start working sequentially:

*   **Architect Step**: You will see the agent analyzing your request. The resulting **Execution Plan** will be displayed, showing the files it intends to create.
*   **Coder Step**: The agent will start writing code for each file defined in the plan. You can see the code being generated in real-time or as it completes.
*   **Reviewer Step**: The system will attempt to run the generated code.
    *   **Success**: You will see a green "PASSED" or "Approved" message.
    *   **Failure**: You will see error logs. The system will automatically loop back to the **Coder** agent to fix the errors based on the feedback.

### 3. Viewing Results
*   **Generated Files**: The code is written directly to your workspace (usually in the root or a specified `generated/` folder, depending on configuration).
*   **Logs**: The UI displays the conversation history and actions taken by each agent.

## Tips for Best Results

*   **Be Specific**: The **Architect** relies on your description. The more identifying details you provide (libraries to use, input/output formats), the better the plan.
*   **Simple Tasks First**: Start with smaller, self-contained scripts to test the system's capabilities before moving to complex multi-file projects.
*   **Check Console**: If something hangs, check the terminal where you ran `streamlit run app.py` for backend logs or errors.

## Troubleshooting

*   **"Model not found"**: Ensure you have pulled the correct models using `ollama pull <model_name>`.
*   **Slow Generation**: Local LLMs are resource-intensive. Performance depends heavily on your GPU/CPU.
*   **Infinite Loops**: If the Coder fails to fix an error after 3 attempts, the system will stop. Check the logs to see why the fix isn't working (e.g., missing system dependency).
