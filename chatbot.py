import streamlit as st
from streamlit import session_state as state

import llm

from utils import *

import pandas as pd
import time


def start() :
    st.markdown("<h1 style='text-align: center;'>AI chat</h1>", unsafe_allow_html=True)
    # hr()
    
    # Initializing chat #
    if 'chat' not in state:
        state['chat'] = [{
            'role': 'assistant',
            'content': ['Hey!','How can I help you?']
        }]

    # Displaying all the messages #
    for msg in state['chat']:
        with st.chat_message(msg['role']) :
            for content in msg['content'] :
                st.write(content)

    # Input box #
    prompt = st.chat_input('Ask us anything!')

    # Posint the question #
    if prompt and state['chat'][-1]['role'] == 'assistant' :
        # Posting user's prompt #
        state['chat'].append({
            'role': 'user',
            'content': [prompt]
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
        st.rerun()
