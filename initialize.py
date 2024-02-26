import streamlit as st
from streamlit import session_state as state

import pandas as pd
import datetime

from google.cloud import firestore

from utils import *

def init(restart=False) :
	####################################
	# Creating initial state variables #
    bool_states = ['logged_in', 'register', 'username','user_found','user_type','current_page']
    
    for _ in bool_states :
        if _ not in state :
            state[_] = False

    if 'layout' not in state :
        state['layout'] = 'centered'

    ###################################
    # Applying Styles #
    main_styles()

    ###################################
    # Connecting to FireStore
    # Authenticate to Firestore with the JSON account key.
    db = firestore.Client.from_service_account_json("mono-ai.json")

    collections = ['users_db','auth_code','login_queries']

    for _ in collections :
        if _ not in state or restart == True :
            state[_] = db.collection(_)


###############################################################
def main_styles() :
	# Adding some style #
	st.set_page_config(page_title='Mono-Analysis', page_icon='🤖', layout = state['layout'])
	st.markdown("""<style>div.stButton > button:first-child {background-color: rgb(0, 153, 204);} </style>""", unsafe_allow_html=True)


###############################################################
def width_settings(key: str) :
    if key == 'Home' :
        set_to_wide()
    elif key == 'Data' :
        set_to_wide()
    elif key == 'AI Assistant' :
        set_to_standard()