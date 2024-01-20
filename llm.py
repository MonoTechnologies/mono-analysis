import streamlit as st
from streamlit import session_state as state
import time

def get_response(prompt) :
    time.sleep(2)
    return "Hello!!"


def interpret(prompt) :
    if prompt.lower() == 'clear' :
        state['chat'] = [state['chat'][0]]
        st.rerun()

    return get_response(prompt)