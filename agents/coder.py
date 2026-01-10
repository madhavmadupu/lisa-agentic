from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from tools.file_manager import write_file
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
        
        prompt = ChatPromptTemplate.from_template(
            """
            You are an Expert Python Developer.
            Implement the following file based on the description.
            
            Filename: {filename}
            Description: {description}
            
            Return ONLY the code. No markdown, no comments outside the code.
            """
        )
        
        chain = prompt | llm
        try:
            code = chain.invoke({"filename": filename, "description": description})
            
            # Clean up code (remove markdown backticks if present)
            clean_code = code.content.replace("```python", "").replace("```", "").strip()
            
            # Write to workspace
            result = write_file(filename, clean_code)
            generated_code_log.append(f"File: {filename} - {result}")
            
        except Exception as e:
            generated_code_log.append(f"File: {filename} - Error: {str(e)}")
            
    return {"code": "\n".join(generated_code_log)}
