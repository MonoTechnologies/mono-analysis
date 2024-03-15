import streamlit as st
from streamlit import session_state as state

import time

def init() :
	####################################
	# Creating initial state variables #
    bool_states = ['current_page']
    
    for _ in bool_states :
        if _ not in state :
            state[_] = False
    
    int_states = ['editor_key_datatypes']
    for _ in int_states :
        if _ not in state :
            state[_] = 0

    list_states = ['chart_views']
    for _ in list_states :
        if _ not in state :
            state[_] = []

    if 'layout' not in state :
        state['layout'] = 'wide'

    ###################################
    # Applying Styles #
    main_styles()


###############################################################
def main_styles() :
	# Adding page configuration #
    st.set_page_config(page_title='Mono-Analysis', page_icon='🏛', layout = state['layout'])

    # Changing button styles #
    st.markdown("""<style>div.stButton > button:first-child {background-color: rgb(0, 153, 204);} </style>""", unsafe_allow_html=True)

    # Removing the extra space from the top #
    st.markdown("""<style>.block-container {padding-top: 0rem;}</style>""", unsafe_allow_html=True)
    
###############################################################

def set_to_wide() :
    state['layout'] = 'wide'

def set_to_standard() :
    state['layout'] = 'centered'


def width_settings(arg) :
    if state[arg] == 'Home' :
        set_to_wide()
    elif state[arg] == 'Data' :
        set_to_wide()
    elif state[arg] == 'Analysis' :
        set_to_wide()
    elif state[arg] == 'AI Assistant' :
        set_to_standard()
###############################################################