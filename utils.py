import pandas as pd
import numpy as np

import streamlit as st
from streamlit import session_state as state


def read_file() :
    # Uploading file button #
    uploaded_file = st.file_uploader('Upload a tabular data')

    # Showing it to the user #
    if uploaded_file != None and 'original_df' not in state :
        # Converting it to Pandas DataFrame #
        # original_df = pd.read_excel(uploaded_file) # Experimental
        state['original_df'] = pd.read_excel('data.xlsx')

        # Appending it to our chat #
        state['chat'].append({
            'role': 'assistant',
            'content': [ 'Successfully uploaded!', state['original_df'] ] 
        })