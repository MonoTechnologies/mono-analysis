import streamlit as st
from streamlit import session_state as state

from utils import *

def data_section() :
    # Getting the data #
    read_file()
    
    # Asking for options #
    data_prep_enabled = st.toggle('Data preparation', value=True)
    analysis_enabled = st.toggle('Data analysis', value=True)
    
    predicting_enabled = st.toggle('Predicting (Premium)', value=False, disabled=True)