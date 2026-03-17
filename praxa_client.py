import streamlit as st
import praxa_rag
import random
import time

st.set_page_config(
    page_title="Praxa",
    page_icon="🎭",
    layout="centered"
)

st.title("🎭 Praxa")
st.caption("Ask me anything about West End and Broadway theatre.")
with st.sidebar:
    st.markdown("### About Praxa")
    st.markdown("Praxa uses RAG to answer questions about West End and Broadway theatre, grounded in real source documents.")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Accept user input
if prompt := st.chat_input("What is up?"):
    # Add user message to chat history
    question = prompt
    st.session_state.messages.append({"role": "user", "content": prompt})
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(question)

    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        response =praxa_rag.answer_and_sources(question)
        st.markdown(response["answer"])
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": response["answer"]})