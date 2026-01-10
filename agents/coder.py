from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from tools.file_manager import write_file, read_file
import os

# Initialize the model
llm = ChatOllama(model="qwen2.5-coder:7b", temperature=0.2)

def coder_node(state):
    """
    The Coder Agent: Takes the plan and writes the code.
    """
    print("--- Coder Agent ---")
    plan = state['plan']
    
    if not plan:
        return {"code": None, "error": "No plan provided."}
    
    generated_code_log = []
    
    for file_info in plan.get('files', []):
        filename = file_info['filename']
        description = file_info['description']
        
        # Check if this is a retry/fix attempt
        feedback = state.get('review_feedback')
        execution_output = state.get('execution_output')
        is_retry = feedback and feedback != "Approved" and execution_output
        
        if is_retry:
            # RETRY MODE: Fix existing code
            current_code_content = read_file(filename)
            if "Error" in current_code_content: # fallback if file read failed
                current_code_content = "# Error reading file, writing fresh."

            prompt = ChatPromptTemplate.from_template(
                """
                You are an Expert Python Developer.
                Argument: The following code has failed execution.
                
                Filename: {filename}
                Description: {description}
                
                Current Code:
                {current_code}
                
                Errors / Feedback:
                {feedback}
                {execution_log}
                
                Task: Fix the code to resolve the errors.
                Return ONLY the fixed code. No markdown, no comments outside the code.
                """
            )
            input_dict = {
                "filename": filename, 
                "description": description,
                "current_code": current_code_content,
                "feedback": feedback,
                "execution_log": execution_output
            }
            
        else:
            # FRESH MODE: Create new code
            prompt = ChatPromptTemplate.from_template(
                """
                You are an Expert Python Developer.
                Implement the following file based on the description.
                
                Filename: {filename}
                Description: {description}
                
                Return ONLY the code. No markdown, no comments outside the code.
                """
            )
            input_dict = {"filename": filename, "description": description}
        
        chain = prompt | llm
        try:
            code = chain.invoke(input_dict)
            
            # Clean up code (remove markdown backticks if present)
            clean_code = code.content.replace("```python", "").replace("```", "").strip()
            
            # Write to workspace
            result = write_file(filename, clean_code)
            action_type = "FIXED" if is_retry else "GENERATED"
            generated_code_log.append(f"{action_type} File: {filename} - {result}")
            
        except Exception as e:
            generated_code_log.append(f"File: {filename} - Error: {str(e)}")
            
    return {"code": "\n".join(generated_code_log)}
