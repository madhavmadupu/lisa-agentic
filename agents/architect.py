from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser
import json

# Initialize the model (removed global init)

def architect_node(state):
    """
    The Architect Agent: Analyzes the user request and creates an execution plan.
    """
    print("--- Architect Agent ---")
    user_request = state['user_request']
    model_name = state.get('architect_model', "llama3.1:8b")
    
    try:
        llm = ChatOllama(model=model_name, temperature=0, base_url="http://127.0.0.1:11434")
        
        prompt = ChatPromptTemplate.from_template(
            """
            You are a Senior Software Architect.
            Analyze the following user request and create a detailed Technical Execution Plan in JSON format.
            
            User Request: {request}
            
            Output format:
            {{
                "files": [
                    {{
                        "filename": "file.py",
                        "description": "What this file does",
                        "dependencies": ["list", "of", "dependencies"]
                    }}
                ],
                "step_by_step_instructions": [
                    "Step 1...",
                    "Step 2..."
                ]
            }}
            
            IMPORTANT:
            - Use RELATIVE paths only (e.g., 'main.py', 'utils/helper.py').
            - DO NOT use absolute paths (e.g., '/app/main.py').
            - DO NOT use drive letters (e.g., 'C:/users/...').
            """
        )
        
        chain = prompt | llm | JsonOutputParser()
        plan = chain.invoke({"request": user_request})
        return {"plan": plan, "error": None}
    except Exception as e:
        print(f"Error in Architect Agent: {e}")
        return {"plan": {}, "error": str(e)}
