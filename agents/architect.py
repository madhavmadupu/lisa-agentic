from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser
import json

# Initialize the model
llm = ChatOllama(model="llama3.1:8b", temperature=0)

def architect_node(state):
    """
    The Architect Agent: Analyzes the user request and creates an execution plan.
    """
    print("--- Architect Agent ---")
    user_request = state['user_request']
    
    prompt = ChatPromptTemplate.from_template(
        """
        You are a Senior Software Architect.
        Analyze the following user request and create a detailed Technical Execution Plan in JSON format.
        
        User Request: {request}
        
        Output format:
        {{
            "files": [
                {{
                    "filename": "path/to/file.py",
                    "description": "What this file does",
                    "dependencies": ["list", "of", "dependencies"]
                }}
            ],
            "step_by_step_instructions": [
                "Step 1...",
                "Step 2..."
            ]
        }}
        """
    )
    
    chain = prompt | llm | JsonOutputParser()
    
    try:
        plan = chain.invoke({"request": user_request})
        return {"plan": plan, "error": None}
    except Exception as e:
        return {"plan": {}, "error": str(e)}
