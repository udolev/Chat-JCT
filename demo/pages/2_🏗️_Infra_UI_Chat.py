import os
import time
import streamlit as st
from PIL import Image

import requests
import json

image = Image.open('./demo/pages/acmelogo.jpeg')
st.set_page_config(
    page_icon=image)

api_url = "http://localhost:8000/api/v1/chat/special_assistant"

logo = Image.open('./demo/pages/acme.jpeg')
st.sidebar.image(logo, width=300)

st.title("Infra-UI LLM Chat")
clear_btn = st.button("clear")

if clear_btn:
    st.session_state.clear()
    st.experimental_rerun()

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])


def display_message(role, content):
    st.markdown(content)
    st.session_state.messages.append({"role": role, "content": content})

# Accept user input
if prompt := st.chat_input("Enter your prompt here..."):
    # Display user message in chat message container
    with st.chat_message("user"):
        display_message("user", prompt)

    with st.spinner('Processing prompt...'):
        query = {"prompt": st.session_state.messages[-1]['content'],
                 "llama_context": "infra_ui"}
        response = requests.post(api_url,json=query)
        if response.status_code != 200:
            chat_response = f'Error: {response.text}'
        else:
            chat_response = response.json()['response']

    with st.chat_message("assistant"):
        display_message("assistant", chat_response)
