import streamlit as st
from streamlit import session_state as state

import llm
import initialize

import pandas as pd
import time

def sidebar() :
    uploaded_file = st.sidebar.file_uploader('Upload a tabular data')

    

def chat() :
    # Initializing chat #
    if 'chat' not in state:
        state['chat'] = [{
            'role': 'assistant',
            'content': 'Hey! How can I help you?'
        }]

    # Displaying all the messages #
    for msg in state['chat']:
        st.chat_message(msg['role']).write(msg['content'])

    # Input box #
    prompt = st.chat_input('Ask us anything!')

    # Posint the question #
    if prompt and state['chat'][-1]['role'] == 'assistant' :
        # Posting user's prompt #
        state['chat'].append({
            'role': 'user',
            'content': prompt
        })

        # Posting user's prompt #
        time.sleep(0.1)
        st.rerun()

    # Getting and posting Response #
    if state['chat'][-1]['role'] == 'user' :
        # Getting user's last request #
        prompt = state['chat'][-1]['content']

        # Getting and posting response #
        with st.spinner('...') :
            response = llm.interpret(prompt)
        
        # Posting the response #
        state['chat'].append({
            'role': 'assistant',
            'content': response
        })

        # Reloading the session to view new messages #
        state['prompt_posted'] = False
        st.rerun()


if __name__ == '__main__':
    initialize.init()

    st.title("💬 Mono-Chat")
    st.caption('🚀 A chatbot powered by LLMs and fine-tuned with your data!')

    sidebar()
    chat()
    