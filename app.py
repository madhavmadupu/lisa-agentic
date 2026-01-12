import streamlit as st
import os
from state.graph import app as graph_app

st.set_page_config(page_title="LISA - Local Intelligence Software Architect", layout="wide")

st.title("LISA: Local Intelligence Software Architect")
st.markdown("### Secure, Air-Gapped Code Generation & Review")

from tools.file_manager import clear_workspace
import shutil

# Sidebar for controls and status
with st.sidebar:
    st.header("⚙️ Configuration")
    
    # Model Selection
    st.subheader("Models")
    architect_model = st.text_input("Architect Model", "llama3.1:8b")
    coder_model = st.text_input("Coder Model", "qwen2.5-coder:7b")
    reviewer_model = st.text_input("Reviewer Model", "mistral-nemo")
    
    st.divider()
    
    st.header("🛠️ Workspace")
    if st.button("Clear Workspace"):
        msg = clear_workspace()
        st.success(msg)

    st.divider()
    
    st.header("Status")
    status_placeholder = st.empty()
    st.info("System Ready")

# User Input
user_request = st.text_area("Enter your development task:", height=150, placeholder="E.g., Create a Python script to parse a CSV file...")

if st.button("Start Agents"):
    if not user_request:
        st.warning("Please enter a request.")
    else:
        st.info("Agents activated...")
        
        # Initial State
        initial_state = {
            "user_request": user_request, 
            "retry_count": 0,
            "architect_model": architect_model,
            "coder_model": coder_model,
            "reviewer_model": reviewer_model
        }
        
        # Run graph
        events = graph_app.stream(initial_state)
        
        # Container for logs
        log_container = st.container()
        
        for i, event in enumerate(events):
            for node, state in event.items():
                
                # Check for errors
                if state.get("error"):
                    st.error(f"Error in {node}: {state.get('error')}")
                
                with log_container.expander(f"Agent: {node.capitalize()}", expanded=True):
                    # customized display based on node
                    if node == "architect":
                        st.json(state.get("plan"))
                    elif node == "coder":
                        st.code(state.get("code"), language="python")
                    elif node == "reviewer":
                        st.text_area("Execution Output", state.get("execution_output"), height=100, key=f"exec_out_{i}")
                        st.write(f"**Feedback:** {state.get('review_feedback')}")

        st.success("Task Complete!")
