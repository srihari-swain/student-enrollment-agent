"""
Streamlit UI for the Student Enrollment Assistant Agent.

Usage:
    streamlit run app.py
"""

import os

import streamlit as st
from dotenv import load_dotenv

from src.agent.enrollment_agent import StudentEnrollmentAgent

load_dotenv()

st.set_page_config(
    page_title="Student Enrollment Assistant",
    page_icon="🎓",
    layout="centered",
)

with st.sidebar:
    st.header("Settings")

    api_key = st.text_input(
        "OpenAI API Key",
        value=os.environ.get("OPENAI_API_KEY", ""),
        type="password",
        placeholder="sk-...",
    )

    model_options = ["gpt-4o-mini", "gpt-4o", "gpt-4", "gpt-3.5-turbo"]
    env_model = os.environ.get("MODEL_NAME", "gpt-4o-mini")
    default_index = model_options.index(env_model) if env_model in model_options else 0

    model = st.selectbox(
        "Model",
        options=model_options,
        index=default_index,
    )

    if st.button("Apply & Reset Chat", use_container_width=True):
        if not api_key:
            st.error("Please enter your OpenAI API key.")
        else:
            st.session_state.agent = StudentEnrollmentAgent(
                openai_api_key=api_key, model=model,
            )
            st.session_state.messages = []
            st.session_state.configured = True
            st.rerun()

if "messages" not in st.session_state:
    st.session_state.messages = []

if "agent" not in st.session_state:
    if api_key:
        st.session_state.agent = StudentEnrollmentAgent(
            openai_api_key=api_key, model=model,
        )
        st.session_state.configured = True
    else:
        st.session_state.configured = False

st.markdown(
    """
    <div style="text-align:center; padding: 20px 0 10px 0;">
        <h2>Student Enrollment Assistant</h2>
        <p style="color:gray; font-size:14px;">
            Ask about <b>Programs</b> · <b>Deadlines</b> · <b>Application Status</b>
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)

if not st.session_state.get("configured"):
    st.info("Enter your OpenAI API key in the sidebar to get started.")
    st.stop()

for msg in st.session_state.messages:
    avatar = "🧑‍🎓" if msg["role"] == "user" else "🤖"
    with st.chat_message(msg["role"], avatar=avatar):
        st.markdown(msg["content"])

if user_input := st.chat_input("Ask a question..."):
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user", avatar="🧑‍🎓"):
        st.markdown(user_input)

    with st.chat_message("assistant", avatar="🤖"):
        with st.spinner("Thinking..."):
            response = st.session_state.agent.chat(user_input)
        st.markdown(response)

    st.session_state.messages.append({"role": "assistant", "content": response})
