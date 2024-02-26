import streamlit as st
from streamlit import session_state as state
from streamlit_option_menu import option_menu

import initialize
import login
from utils import *
from landing import *
from data_prep import *
from chat import *

import pandas as pd
import time



def show_sidebar() :
    ############################################
    # Option Menu docs : https://github.com/victoryhb/streamlit-option-menu
    # Icon store : https://icons.getbootstrap.com/

    button = option_menu(
        menu_title = 'Mono-AI',
        options = ["Home", "Data", "Analysis", 'AI Assistant', 'Settings'],
        icons = ['house', 'cloud-plus', "graph-up", 'robot', 'gear'],
        key = 'main_menu',
        orientation="vertical"
    )
    ############################################

    if state['current_page'] != button :
        state['current_page'] = button
        initialize.width_settings(button)
        st.rerun()



def show_pages() :
    ############################################
    if state['current_page'] == 'Home' :
        home_section()
    elif state['current_page'] == 'Data' :
        data_section()
    elif state['current_page'] == 'AI Assistant' :
        chat_section()



if __name__ == '__main__':
    # Initializing session variables and basic functions #
    initialize.init()

    # Login Page #
    login.check_register()
    login.check_login()

    # st.write( get_docs('users_db') )

    # Displaying Menu #
    with st.sidebar :
        show_sidebar()

    # Displaying the current page #
    show_pages()

     # # Initializing databases #
    # with st.spinner( 'Deleting databases\' values' ) :
    #     databases_ = [ 'debt_queries', 'login_queries', 'product_queries', 'products_db', 'customers_debt', 'providers_debt' ]
    #     for db in databases_ :
    #         reset_( db )