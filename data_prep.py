import streamlit as st
from streamlit import session_state as state
import time

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
        perform_general_processing()

    ##################################################################################
    # Column types module #
    if column_types and 'original_df' in state :
        st.divider()



########################################################################################################################
########################################################################################################################
def perform_general_processing() :
    st.subheader(':blue[General processing module]')
    with st.expander('Columns to remove') :
        # Recommending to remove columns with a lot of Nones #
        none_columns = []
        for col in state['preprocessed_df'] :
            null_values_sum = state['preprocessed_df'][col].isna().sum()
            nulls_threshold = 40 #len(state['original_df'])/2

            if null_values_sum >= nulls_threshold :
                none_columns.append((col,null_values_sum))

        if len(list(none_columns)) :
            default_nones = list(zip(*none_columns))[0]
        else :
            default_nones = []

        removal_choices = st.multiselect(
            label = 'Choose unused columns or columns with a lot of None values to remove',
            options = state['preprocessed_df'].columns,
            default = default_nones
        )
        # Submitting column removal #
        st.button(
            label='Remove columns',
            key='submit_remove_columns'
        )
        if state['submit_remove_columns'] :
            state['preprocessed_df'].drop(removal_choices,axis=1,inplace=True,errors='ignore')
            st.success('Columns successfully removed!')
            time.sleep(1.5)
            st.rerun()


    # Choosing data batch #
    with st.expander('Choosing Data batch') :
        st.toggle('Choose Entire Dataset', value=True, key='entire_dataset_toggle')

        if not state['entire_dataset_toggle'] :
            hr()
            #############################
            # Choosing filtering method #
            batch_filtering_method = st.radio(
                label = 'Filtering method',
                options = ['Random subset', 'Choose by index', 'Seperate by date'],
                horizontal=True
            )
            ##################################################
            # batch_filtering_method: Random subset batching #
            if batch_filtering_method == 'Random subset' :
                hr()
                with st.columns(2)[0] :
                    proportion_of_random_batch = st.slider(
                        label='Pick a proportion of the new Random subset',
                        min_value=1,
                        max_value=99,
                        value=50
                    )
                # Submit new random subset fraction #
                submit_random_batching = st.button('Filter new random subset')
                if submit_random_batching :
                    state['preprocessed_df'] = state['preprocessed_df'].sample(frac=proportion_of_random_batch/100)
                    state['preprocessed_df'].reset_index(inplace=True, drop=True)
                    st.success(f'Successfully filtered and left {proportion_of_random_batch}% of rows!')
                    time.sleep(2)
                    st.rerun()

            #########################################
            # batch_filtering_method: Choose by index
            elif batch_filtering_method == 'Choose by index' :
                hr()
                cols = st.columns(8)
                with cols[0] :
                    lower_bound = st.number_input(
                        label='Left boundary',
                        placeholder='Min: 0',
                        value=None,
                        min_value=0,
                        max_value = len(state['preprocessed_df'])-1
                    )

                with cols[1] :
                    preprocessed_df_length = len(state['preprocessed_df'])
                    upper_bound = st.number_input(
                        label='Right boundary',
                        placeholder=f'Max: {preprocessed_df_length-1}',
                        value=None,
                        min_value=0,
                        max_value = len(state['preprocessed_df'])-1
                    )

                submit_index_batching = st.button('Filter and leave the given range')

                # Submitting Random Batching #
                if submit_index_batching :
                    state['preprocessed_df'] = state['preprocessed_df'][ (state['preprocessed_df'].index >= lower_bound) 
                                                                        & (state['preprocessed_df'].index <= upper_bound) ]
                    st.success('Successfully filtered and left only the given range!')
                    time.sleep(1.5)
                    st.rerun()




    # Printing out the preprocessed dataframe #
    if 'preprocessed_df' in state :
        hr()
        st.subheader('Preprocessed data:')
        st.write(state['preprocessed_df'].head(200))