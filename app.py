import streamlit as st
import os
import sys

sys.path.append(os.path.abspath(os.path.dirname(__file__)))
from tcc_platform.graph import build_graph

st.set_page_config(page_title="TCC Config Chatbot", layout="wide")

st.title("TCC Config Platform")
st.markdown("Natural Language Authoring for Tracking Content Configurations")

if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("E.g., Change the message for standard inbound leg1 exceptions to say there is a weather delay."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Processing request through Agent Pipeline..."):
            try:
                graph = build_graph()
                initial_state = {"request": prompt, "iterations": 0}
                final_state = graph.invoke(initial_state)
                
                response_md = f"**Final Status:** {final_state.get('status')}\n\n"
                
                if final_state.get("target_rule"):
                    response_md += f"**Target Rule Identified:**\n```json\n{final_state['target_rule']}\n```\n"
                
                if final_state.get("patch_data"):
                    response_md += f"**Proposed Changes:**\n```json\n{final_state['patch_data']}\n```\n"
                    
                if final_state.get("validation_errors"):
                    response_md += f"**Validation Errors:**\n"
                    for e in final_state["validation_errors"]:
                        response_md += f"- {e}\n"
                        
                if final_state.get("pr_url"):
                    response_md += f"🎉 **Change applied and PR raised:** [View Pull Request]({final_state['pr_url']})"
                
                st.markdown(response_md)
                st.session_state.messages.append({"role": "assistant", "content": response_md})
            except Exception as e:
                error_msg = f"Error processing request: {str(e)}"
                st.error(error_msg)
                st.session_state.messages.append({"role": "assistant", "content": error_msg})
