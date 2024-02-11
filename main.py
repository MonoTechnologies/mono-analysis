import streamlit as st
from streamlit import session_state as state

import initialize
import llm

from utils import *
from landing import *
from data_prep import *
from chat import *

import pandas as pd
import time


def show_sidebar() :
    ############################################
    buttons = {}

    buttons['landing'] = st.button('Main Page')
    hr()
    buttons['data'] = st.button('Your Data')
    buttons['analysis'] = st.button('Analysis')
    buttons['chat'] = st.button('Chat-Assistant')

    ############################################

    for button in buttons :
        if buttons[button] == True and state['current_page'] != button :
            state['current_page'] = button
            st.experimental_rerun()

    # Setting do default #
    if state['current_page'] == False :
        state['current_page'] = 'landing'
        st.experimental_rerun()



def show_pages() :
    ############################################
    if state['current_page'] == 'landing' :
        main_page()
    elif state['current_page'] == 'data' :
        data_section()
    elif state['current_page'] == 'chat' :
        chat_section()



if __name__ == '__main__':
    # Initializing session variables and basic functions #
    initialize.init()

    # Displaying Menu #
    with st.sidebar :
        show_sidebar()

    # Displaying the current page #
    show_pages()