import streamlit as st
from streamlit import session_state as state

import llm
import initialize

import pandas as pd
import time

def wiki_section() :
    with st.expander('Want to learn more?') :
        st.write('Fuck off!')




def data_section() :
    uploaded_file = st.file_uploader('Upload a tabular data')
    
    data_prep_enabled = st.toggle('Data preparation', value=True)
    analysis_enabled = st.toggle('Data analysis', value=True)
    
    predicting_enabled = st.toggle('Predicting (Premium)', value=False, disabled=True)

    

def chat_section() :
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
    # Initializing session variables and basic functions #
    initialize.init()

    # Showing the title #
    st.title("💬 Mono-Chat")

    # Showing the wiki section #
    wiki_section()

    # Showing the Data management section #
    with st.sidebar:
        data_section()
    
    # Showing the chat section #
    chat_section()