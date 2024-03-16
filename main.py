import pandas as pd
import time

import streamlit as st
from streamlit import session_state as state
from streamlit_option_menu import option_menu

import initialize
import login
import landing
import data_prep
import chatbot
import analysis
from utils import *


def show_sidebar() :
    ############################################
    # Option Menu docs : https://github.com/victoryhb/streamlit-option-menu
    # Icon store : https://icons.getbootstrap.com/

    side_button = option_menu(
        menu_title = 'Mono-AI',
        options = ["Home", 'Profile', 'Settings', '---' , "Data", "Analysis", 'AI Assistant'],
        icons = ['house', 'person-circle', 'gear', '---', 'cloud-plus', "graph-up", 'robot'],
        key = 'main_menu',
        orientation="vertical",
        on_change = initialize.width_settings
    )
    ############################################

    if state['current_page'] != side_button :
        state['current_page'] = side_button
        st.rerun()



def show_pages() :
    ############################################
    if state['current_page'] == 'Home' :
        landing.start()
    elif state['current_page'] == 'Data' :
        data_prep.start()
    elif state['current_page'] == 'Analysis' :
        analysis.start()
    elif state['current_page'] == 'AI Assistant' :
        chatbot.start()



if __name__ == '__main__':
    # Initializing session variables and basic functions #
    initialize.init()

    # Login Page #
    # login.check()

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