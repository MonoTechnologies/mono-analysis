import streamlit as st
from streamlit import session_state as state

import llm

import pandas as pd

def sidebar() :
    uploaded_file = st.sidebar.file_uploader('Upload a tabular data')

    

def chat() :
    # Initializing chat #
    if 'chat' not in state:
        state['chat'] = [{
            'role': 'assistant',
            'content': 'How can I help you?'
        }]

    # Displaying all the messages #
    for msg in state['chat']:
        st.chat_message(msg['role']).write(msg['content'])

    # Input box #
    prompt = st.chat_input('Ask us anything!')

    # Triggered when question is requested #
    if prompt:
        # Posting user's prompt #
        state['chat'].append({
            'role': 'user',
            'content': prompt
        })

        # Getting and posting response #
        response = llm.get_response(prompt)
        
        # Posting the response #
        state['chat'].append({
            'role': 'assistant',
            'content': response
        })

        # Reloading the session to view new messages #
        st.rerun()


if __name__ == '__main__':
    st.title("💬 Mono-Chat")
    st.caption('🚀 A chatbot powered by OpenAI LLM')

    sidebar()
    chat()
    