import streamlit as st
from streamlit import session_state as state

from utils import *

def data_section() :
    st.title('Data Factory')
    
    #################################################################################
    # Uploading data and showing basic info #
    st.divider()
    st.subheader('Data Uploading')

    # Getting the data #
    read_file()
    
    # If data uploaded #
    if 'original_df' in state :
        with st.expander('Uploaded data ✅') :
            st.divider()
            st.subheader('Overview:')
            st.write(state['original_df'].head(300))
            st.divider()
            st.subheader('Column info:')
            st.write( state['original_df'].describe().drop(['25%','50%','75%']).T )

    #################################################################################
    # Asking for options #
    st.divider()
    st.subheader('Preprocessing')

    data_prep_enabled = st.toggle('Data preparation', value=True)
    analysis_enabled = st.toggle('Data analysis', value=True)
    predicting_enabled = st.toggle('Predicting (Premium)', value=False, disabled=True)

    ##################################################################################
    # Data preparation module #
    st.divider()
    if data_prep_enabled and 'original_df' in state :
        with st.form('Data') :
            st.subheader('Data Preparation module')
            # st.write( list(state['original_df'].columns) )
            st.form_submit_button('Submit')

    if analysis_enabled and 'original_df' in state :
        with st.form('Analysis_of data') :
            st.subheader('Data Analysis module')
            # st.write( list(state['original_df'].columns) )
            st.form_submit_button('Submit')