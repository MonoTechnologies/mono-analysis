import streamlit as st
from streamlit import session_state as state

def init() :
    bool_states = []
    
    for _ in bool_states :
        if _ not in state :
            state[_] = False



def main_styles() :
	# Adding some style #
	st.set_page_config(page_title='Mono-Analysis', page_icon='🏛', layout = state['layout'])
	st.markdown("""<style>div.stButton > button:first-child {background-color: rgb(0, 153, 204);} </style>""", unsafe_allow_html=True)
     

def set_to_wide() :
	state['layout'] = 'wide'

def set_to_standard() :
	state['layout'] = 'centered'