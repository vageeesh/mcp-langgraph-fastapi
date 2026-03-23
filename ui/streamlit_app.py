import streamlit as st
import requests
import pandas as pd
import json

API_URL = "http://0.0.0.0:8000"
# If i Dockerise this, then update URL to 'API_URL = "http://api:8000"' because docker to docker communication via service name

st.title("Admin Reporting UI")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

prompt = st.chat_input("Ask something")

if prompt:
    st.session_state.messages.append(
        {"role": "user", "content": prompt}
    )

    with st.chat_message("user"):
        st.write(prompt)

    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        
        with requests.post(
            f"{API_URL}/query/stream",
            json={"query": prompt},
            stream=True
        ) as response:
            for line in response.iter_lines():
                if line:
                    chunk = line.decode('utf-8')
                    full_response += chunk
                    # Append cursor to indicate streaming response (optional, can be removed if not desired)
                    message_placeholder.markdown(full_response + "▌")
                        
            # Remove cursor after streaming is complete
            message_placeholder.markdown(full_response)
    
    st.session_state.messages.append(
        {"role": "assistant", "content": full_response}
    )

if st.button("Clear Chat"):
    st.session_state.messages = []