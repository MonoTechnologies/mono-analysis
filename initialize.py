import streamlit as st
from streamlit import session_state as state

import pandas as pd
import datetime

from utils import *

def init() :
	####################################
	# Creating initial state variables #
    bool_states = ['current_page']
    
    for _ in bool_states :
        if _ not in state :
            state[_] = False

    if 'layout' not in state :
        state['layout'] = 'wide'

    ###################################
    # Applying Styles #
    main_styles()


###############################################################
def main_styles() :
	# Adding some style #
	st.set_page_config(page_title='Mono-Analysis', page_icon='🤖', layout = state['layout'])
	st.markdown("""<style>div.stButton > button:first-child {background-color: rgb(0, 153, 204);} </style>""", unsafe_allow_html=True)


###############################################################