import streamlit as st
from streamlit import session_state as state
from streamlit_option_menu import option_menu

from utils import *

def start() -> None :
	st.markdown("<h1 style='text-align: center;'>Settings</h1>", unsafe_allow_html=True)
	
	settigs_page = option_menu(
		menu_title = None,
		options = ['Data-Prep', 'Analysis', 'Predictors', 'AI-Chat'],
		icons = ['database', 'pie-chart', 'eye', 'robot'],
		key = 'analysis_section',
		orientation="horizontal"
	)

	if settigs_page == 'Data-Prep' :
		interface()


def interface() -> None :
	space(3)
	st.toggle('Advanced mode')
	space(3)
	st.toggle('Hard reset')
	space(3)
	st.toggle('Excel only', value=True)