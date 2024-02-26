import streamlit as st
from streamlit import session_state as state

from utils import *

def data_section() :
    st.title('Data Factory')
    
    #################################################################################
    # Uploading data and showing basic info #
    st.divider()
    # st.subheader('Data Uploading')

    # Data Uploader #
    read_file()
    
    # Data Info #
    if 'original_df' in state :
        with st.expander('Uploaded data ✅') :
            st.divider()
            st.subheader('Overview:')
            st.write(state['original_df'].head(200))
            st.divider()
            st.subheader('Column info:')
            st.write( state['original_df'].describe().drop(['25%','50%','75%']).T )

    #################################################################################
    # Asking for options #
    st.divider()
    st.subheader('Preprocessing')

    general_processing = st.toggle('General processing', value=True)
    column_types = st.toggle('Column types', value=False)

    ##################################################################################
    # General processing module #
    if general_processing and 'original_df' in state :
        st.divider()
        with st.form('general_processing') :
            st.subheader('General processing module')
            st.form_submit_button('Submit')

    ##################################################################################
    # Column types module #
    if column_types and 'original_df' in state :
        st.divider()
        with st.form('column_types') :
            st.subheader('Column types module')
            st.form_submit_button('Submit')