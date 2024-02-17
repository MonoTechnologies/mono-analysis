import streamlit as st
from streamlit import session_state as state

import initialize
from utils import *
from landing import *
from data_prep import *
from chat import *

import pandas as pd
import time


def show_sidebar() :
    ############################################
    buttons = {}

    buttons['landing'] = st.button('Main Page', on_click=set_to_wide)
    hr()
    buttons['data'] = st.button('Your Data', on_click=set_to_wide)
    buttons['analysis'] = st.button('Analysis',on_click=set_to_wide)
    buttons['chat'] = st.button('Chat-Assistant',on_click=set_to_standard)

    ############################################

    for button in buttons :
        if buttons[button] == True and state['current_page'] != button :
            state['current_page'] = button
            st.rerun()

    # Setting do default #
    if state['current_page'] == False :
        state['current_page'] = 'landing'
        st.rerun()



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