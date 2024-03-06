import pandas as pd
import time

import streamlit as st
from streamlit import session_state as state
from streamlit_option_menu import option_menu
from streamlit_extras.dataframe_explorer import dataframe_explorer

import pandas_profiling
from pandas_profiling import ProfileReport
from streamlit_pandas_profiling import st_profile_report

from utils import *

################################################################
################################################################
def analysis_section() -> None :
	st.header('Data Analysis')

	# Choosing analysis type #
	analysis_button = option_menu(
		menu_title = None,
		options = ["General", "Manual charts", "Pandas Profiling", 'AI assistant'],
		icons = ['bar-chart-fill', 'search', "clipboard-data", 'robot', 'gear'],
		key = 'analysis_section',
		orientation="horizontal"
	)

	# Checking if the dataset was uploaded #
	if 'preprocessed_df' not in state :
		st.info('Please upload a Dataset first')
		st.stop()

	hr()
	if analysis_button == 'General' :
		perform_general_analysis()
	elif analysis_button == 'Pandas Profiling' :
		perform_pandas_profiling()


################################################################
################################################################
def perform_general_analysis() -> None :

    # Asking for filtering options #
    st.subheader('Dataset view:')
    with st.expander('Filter dataset:') :
        state['filtered_df'] = dataframe_explorer( indexed( latest(state['preprocessed_df']) ), case=False)

    # Showing the filtered dataset #
    st.dataframe(state['filtered_df'])

    # Calculating the metrics #
    num_cols, cat_cols, date_cols = [], [], []
    for col in state['filtered_df'].columns :
        if state['filtered_df'][col].dtype in ['int','float'] :
            num_cols.append(col)
        elif state['filtered_df'][col].dtype in ['str', 'object'] :
            cat_cols.append(col)
        elif state['filtered_df'][col].dtype in ['datetime64','datetime64[ns]'] :
            date_cols.append(col)

    # Displaying shape and column types #
    cols = st.columns(2)
    with cols[0] :
        st.info( f"Dataset contains: :green[{state['filtered_df'].shape[0]}] rows and :green[{state['filtered_df'].shape[1]}] columns" )
        
        total_cells = state['filtered_df'].shape[0]*state['filtered_df'].shape[1]
        total_nans = state['filtered_df'].isna().sum().sum()
        nans_percent = round(total_nans/total_cells*100,1)

        st.info( f"In total :green[{total_cells}] cells, where :green[{total_nans}] (:green[{nans_percent}%]) are empty" )

    with cols[1] :
        st.info( f"Column types: :green[{len(num_cols)}] Numerical, :green[{len(cat_cols)}] Categorical and :green[{len(date_cols)}] DateTime" )


    # Data description #
    hr()
    st.subheader('Data description:')
    st.dataframe( state['filtered_df'].describe().drop(['25%','50%','75%']).T, use_container_width=True)

    # Null values #
    hr()
    st.subheader('Null values (Empty cells)')
    st.table( state['filtered_df'].isna().sum() )


################################################################
################################################################
def perform_pandas_profiling() -> None :

	st.info('Pandas Profiling is a detailed explanation of your Data. Thus it can take some time to generate.')
	generate_profiling_button = st.button('Generate Pandas Profiling')

	if 'pandas_profiling' in state :
		state['pandas_profiling']

	if generate_profiling_button :
		pr = state['filtered_df'].profile_report()
		# state['pandas_profiling'] = st_profile_report(pr)