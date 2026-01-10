from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from tools.executor import execute_python
import os

# Initialize the model
llm = ChatOllama(model="mistral-nemo", temperature=0)

def reviewer_node(state):
    """
    The Reviewer Agent: Runs code, checks errors, and provides feedback.
    """
    print("--- Reviewer Agent ---")
    plan = state['plan']
    
    feedback_log = []
    has_errors = False
    
    # Iterate through files in the plan to test them
    for file_info in plan.get('files', []):
        filename = file_info['filename']
        ex_res = execute_python(filename)
        
        if ex_res['return_code'] != 0:
            has_errors = True
            error_msg = ex_res['stderr']
            feedback_log.append(f"File {filename} FAILED:\n{error_msg}")
        else:
            feedback_log.append(f"File {filename} PASSED execution.")
    
    # If errors, ask Mistral to summarize what needs fixing
    if has_errors:
        error_context = "\n".join(feedback_log)
        prompt = ChatPromptTemplate.from_template(
            """
            You are a QA Engineer. The following code execution failed.
            Analyze the errors and provide a concise instruction for the Coder to fix them.
            
            Errors:
            {errors}
            
            Feedback:
            """
        )
        chain = prompt | llm
        feedback_response = chain.invoke({"errors": error_context})
        return {
            "review_feedback": feedback_response.content,
            "execution_output": error_context,
            "retry_count": state.get("retry_count", 0) + 1
        }
    
    return {
        "review_feedback": "Approved",
        "execution_output": "\n".join(feedback_log),
        "retry_count": state.get("retry_count", 0)
    }
