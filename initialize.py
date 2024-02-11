import streamlit as st
from streamlit import session_state as state

def init() :
	####################################
	# Creating initial state variables #
    bool_states = ['current_page']
    
    for _ in bool_states :
        if _ not in state :
            state[_] = False

    state['layout'] = 'centered'

    ###################################
    # Applying Styles #
    main_styles()


###############################################################
def main_styles() :
	# Adding some style #
	st.set_page_config(page_title='Mono-Analysis', page_icon='🏛', layout = state['layout'])
	st.markdown("""<style>div.stButton > button:first-child {background-color: rgb(0, 153, 204);} </style>""", unsafe_allow_html=True)

def set_to_wide() :
	state['layout'] = 'wide'

def set_to_standard() :
	state['layout'] = 'centered'

###############################################################

def indexed( data ) :
	data_copy = data.copy()
	data_copy.index = range( 1, len(data_copy) + 1 )
	return data_copy

def latest( data ) :
	data['время'] = pd.to_datetime(data['время'])
	data = data.sort_values('время',ascending=False)

	return data

def current_time() :
	return pd.to_datetime( datetime.now() ).round('1s')


###############################################################

def hr() :
	st.markdown("<hr>", unsafe_allow_html=True)


def side_hr() :
	st.sidebar.markdown("<hr>", unsafe_allow_html=True)

