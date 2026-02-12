import os
import uuid
import asyncio
import json
from typing import Dict
from fastapi import FastAPI, BackgroundTasks, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from pydantic import BaseModel
from sse_starlette.sse import EventSourceResponse

# Import Agent Graph
from state.graph import app as agent_app

# Import Tools
# Import Tools
from tools.file_manager import read_file
import logging
from database import init_db, create_session, add_message, get_messages, get_all_sessions

from config import config

# Configure logging
logging.basicConfig(
    filename=config.DEBUG_LOG_PATH,
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = FastAPI(title="LISA Agentic API")

@app.on_event("startup")
def startup_event():
    init_db()

# CORS setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8501", "http://127.0.0.1:8501"],  # Restrict to local Streamlit default
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- State Management ---
# In a real app, use Redis/DB. Here we use in-memory queues for streaming.
class AgentSession:
    def __init__(self):
        self.queue = asyncio.Queue()
        self.is_active = True

sessions: Dict[str, AgentSession] = {}

# --- Pydantic Models ---
class AgentRequest(BaseModel):
    user_request: str
    architect_model: str = config.ARCHITECT_MODEL
    coder_model: str = config.CODER_MODEL
    reviewer_model: str = config.REVIEWER_MODEL

class SessionResponse(BaseModel):
    session_id: str

# --- Background Worker ---
async def run_agent_graph(session_id: str, request: AgentRequest):
    session = sessions[session_id]
    logger.info(f"Agent graph started for session {session_id}")
    
    initial_state = {
        "user_request": request.user_request,
        "retry_count": 0,
        "architect_model": request.architect_model,
        "coder_model": request.coder_model,
        "reviewer_model": request.reviewer_model,
        "error": None
    }
    
    try:
        logger.info("Invoking agent_app.astream")
        async for event in agent_app.astream(initial_state):
            logger.info(f"Received event from graph: {list(event.keys())}")
            for node, state in event.items():
                payload = {
                    "node": node,
                    "status": "success",
                    "state": {k: v for k, v in state.items() if k != "plan"} # exclude large plan dump if needed, or include
                }
                # Add specific fields for easier UI parsing
                if node == "architect":
                    payload["plan"] = state.get("plan")
                    if payload["plan"]:
                         plan_text = json.dumps(payload["plan"], indent=2)
                         add_message(session_id, "agent", f"I have created a plan:\n\n{plan_text}", node="architect", meta={"plan": payload["plan"]})
                elif node == "coder":
                    payload["code"] = state.get("code")
                    if payload["code"]:
                        add_message(session_id, "agent", f"I have generated code:\n\n{payload['code']}", node="coder", meta={"code": payload["code"]})
                elif node == "reviewer":
                    payload["feedback"] = state.get("review_feedback")
                    payload["output"] = state.get("execution_output")
                    if payload["feedback"]:
                         add_message(session_id, "agent", f"Reviewer Feedback: {payload['feedback']}\n\nOutput: {payload.get('output', '')}", node="reviewer", meta={"feedback": payload["feedback"], "output": payload["output"]})
                
                await session.queue.put(json.dumps(payload))
                
        # Send completion message
        await session.queue.put(json.dumps({"status": "complete", "message": "Workflow finished."}))
        
    except Exception as e:
        await session.queue.put(json.dumps({"status": "error", "message": str(e)}))
    finally:
        session.is_active = False
        await session.queue.put(None) # Sentinel to stop stream

# --- Endpoints ---

@app.post("/api/agent/run", response_model=SessionResponse)
async def start_agent_run(request: AgentRequest, background_tasks: BackgroundTasks):
    logger.info(f"Received agent run request: {request.user_request}")
    session_id = str(uuid.uuid4())
    sessions[session_id] = AgentSession()
    
    # Start the graph in background
    logger.info(f"Starting background task for session {session_id}")
    
    # Persist session and user message
    create_session(session_id, title=request.user_request[:50])
    add_message(session_id, "user", request.user_request)

    background_tasks.add_task(run_agent_graph, session_id, request)
    
    return SessionResponse(session_id=session_id)

@app.get("/api/agent/stream/{session_id}")
async def stream_agent_events(session_id: str):
    logger.info(f"SSE connection request for session {session_id}")
    if session_id not in sessions:
        logger.error(f"Session {session_id} not found")
        raise HTTPException(status_code=404, detail="Session not found")
        
    session = sessions[session_id]
    
    async def event_generator():
        logger.info(f"Starting event generator for session {session_id}")
        while True:
            # Wait for next event
            data = await session.queue.get()
            
            if data is None:
                logger.info(f"Stream finished for session {session_id}")
                break
                
            logger.info(f"Sending event for {session_id}: {data[:50]}...")
            yield {"data": data}
            
            if not session.is_active and session.queue.empty():
                break

    return EventSourceResponse(event_generator())

@app.get("/api/chat/history/{session_id}")
def get_chat_history(session_id: str):
    return get_messages(session_id)

@app.get("/api/chat/sessions")
def list_sessions():
    return get_all_sessions()

@app.get("/api/workspace/files")
def get_workspace_files():
    """List all files in the workspace recursively."""
    # Assuming list_files returns a formatted string or list. 
    # Let's check typical tool output. standard 'list_dir' tool is different.
    # The 'tools.file_manager.list_files' implementation needs to be verified.
    # If it returns a string, we might want to refactor or parse it.
    # For now, let's wrap it.
    try:
        from tools.file_manager import WORKSPACE_DIR
        
        file_tree = []
        for root, _, files in os.walk(WORKSPACE_DIR):
            for file in files:
                rel_path = os.path.relpath(os.path.join(root, file), WORKSPACE_DIR)
                file_tree.append(rel_path)
                
        return {"files": file_tree}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e

@app.get("/api/workspace/file")
def get_file_content(path: str):
    """Read content of a specific file."""
    content = read_file(path)
    if content.startswith("Error:"):
        raise HTTPException(status_code=400, detail=content)
    return {"content": content}

@app.get("/api/models")
def get_models():
    """Return available models (mocked for now or queried from Ollama)."""
    return {
        "architect": ["llama3.1:8b", "gpt-4", "claude-3-opus"],
        "coder": ["qwen2.5-coder:7b", "deepseek-coder", "gpt-4"],
        "reviewer": ["mistral-nemo", "llama3", "gpt-4"]
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
