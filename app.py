import streamlit as st
import os
from state.graph import app as graph_app

st.set_page_config(page_title="LISA - Local Intelligence Software Architect", layout="wide")

st.title("LISA: Local Intelligence Software Architect")
st.markdown("### Secure, Air-Gapped Code Generation & Review")

# Sidebar for status
with st.sidebar:
    st.header("Agent Status")
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
        initial_state = {"user_request": user_request, "retry_count": 0}
        
        # Run graph
        events = graph_app.stream(initial_state)
        
        # Container for logs
        log_container = st.container()
        
        for event in events:
            for node, state in event.items():
                with log_container.expander(f"Agent: {node.capitalize()}", expanded=True):
                    # customized display based on node
                    if node == "architect":
                        st.json(state.get("plan"))
                    elif node == "coder":
                        st.code(state.get("code"), language="python")
                    elif node == "reviewer":
                        st.text_area("Execution Output", state.get("execution_output"), height=100)
                        st.write(f"**Feedback:** {state.get('review_feedback')}")

        st.success("Task Complete!")
