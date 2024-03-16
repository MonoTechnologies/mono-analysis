import streamlit as st
from streamlit import session_state as state
from streamlit_option_menu import option_menu
from streamlit_extras.dataframe_explorer import dataframe_explorer

import time
import pandas as pd

import io

from utils import *

########################################################################################################################
########################################################################################################################
def start() -> None:
    st.title('Data Factory')

    # Choosing step #
    data_prep_step = option_menu(
        menu_title = None,
        options = ["Upload Data", "General processing", "Column Types", 'Preprocessed Data'],
        icons = ['upload', 'search', "clipboard-data", 'check-circle'],
        key = 'data_prep',
        orientation="horizontal"
    )
    hr()
    if data_prep_step == 'Upload Data' :
        upload_data()
    elif data_prep_step == 'General processing' :
        General_processing()
    elif data_prep_step == 'Column Types' :
        Column_typization()
    elif data_prep_step == 'Preprocessed Data' :
        show_preprocessed()


########################################################################################################################
########################################################################################################################
def upload_data() -> None :
    # Data Uploader #
    read_file()
    
    # Data Info #
    if 'original_df' in state :
        hr()
        st.subheader('Uploaded Dataset ✅')
        st.dataframe(state['original_df'].head(200), use_container_width=True)

        # Data description #
        hr()
        st.subheader('Data description:')

        st.write('Numeric Columns:')
        st.dataframe( state['original_df'].describe().drop(['25%','50%','75%']).T, use_container_width=True)

        st.write('Categorical Columns:')
        st.dataframe( state['original_df'].describe(include='object').T, use_container_width=True )


########################################################################################################################
########################################################################################################################
class General_processing:
    def __init__(self) -> None:
        st.subheader(':blue[General processing module]')

        # Filtering dataset #
        self.filter_dataset()

        # Choosing Data Batch #
        self.batch_data()


    def filter_dataset(self) -> None :
        ################################
        # Asking for filtering options #
        ################################
        with st.expander('Filter dataset:') :
            filtered_df = dataframe_explorer( indexed( latest(state['preprocessed_df']) ), case=False)

            hr()
            # Showing the filtered dataset #
            st.subheader('Filtered dataset')
            st.dataframe(filtered_df)

            # Displaying shape and column types #
            cols = st.columns(2)
            with cols[0] :
                st.info( f"Dataset contains: :green[{filtered_df.shape[0]}] rows and :green[{filtered_df.shape[1]}] columns" )
                total_cells = filtered_df.shape[0]*filtered_df.shape[1]
                total_nans = filtered_df.isna().sum().sum()
                nans_percent = round(total_nans/total_cells*100,1)

            with cols[1] :
                st.info( f"In total :green[{total_cells}] cells, where :green[{total_nans}] (:green[{nans_percent}%]) are empty" )

            apply_filters_button = st.button('Apply filters')
            if apply_filters_button :
                state['preprocessed_df'] = filtered_df
                st.success('Successfully filtered the dataset!')
                time.sleep(1.5)
                st.rerun()


    def batch_data(self) -> None :
        #######################
        # Choosing data batch #
        #######################
        with st.expander('Choosing Data batch:') :
            st.toggle('Choose Entire Dataset', value=True, key='entire_dataset_toggle')

            if not state['entire_dataset_toggle'] :
                hr()
                #############################
                # Choosing filtering method #
                batch_filtering_method = st.radio(
                    label = 'Filtering method',
                    options = ['Random subset', 'Filter by index', 'Filter by date'],
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
                elif batch_filtering_method == 'Filter by index' :
                    hr()
                    cols = st.columns(6)
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


########################################################################################################################
########################################################################################################################
class Column_typization:

    def __init__(self) -> None:
        st.subheader(':green[Column typization module]')

        # Choosing and removing columns #
        self.removing_columns()

        # Changing column types #
        self.column_typing()

        # Setting base date column #
        self.set_base_date_col()

    ##################################################################################################
    def removing_columns(self) -> None :
        ################################
        # Removing unnecessary columns #
        ################################
        with st.expander('Removing columns') :
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


    ##################################################################################################
    def column_typing(self) -> None :
        #############################################
        # Choosing numerical & categorical features #
        #############################################
        with st.expander('Change column types manually') :
            types_mp = {}
            # Finding default numerical features #
            for col in state['preprocessed_df'] :
                if state['preprocessed_df'][col].dtype in ['int64','float64'] :
                    types_mp[col] = 'Numbers 🎲'
            
            # Finding default categorical features #
            for col in state['preprocessed_df'] :
                if state['preprocessed_df'][col].dtype in ['str','object'] :
                    types_mp[col] = 'Categories 🚦'
            
            # Finding default date features #
            for col in state['preprocessed_df'] :
                if state['preprocessed_df'][col].dtype in ['datetime','datetime64','datetime64[ns]'] :
                    types_mp[col] = 'Dates 🗓'

            # Dataframe with all columns with their data types #
            col_types_df = pd.DataFrame()
            col_types_df['Column name'] = state['preprocessed_df'].columns
            col_types_df['Data type'] = [ types_mp[col] for col in state['preprocessed_df'].columns ]

            # Interactive data editor to change data types if needed #
            edited_df = st.data_editor(
                col_types_df,
                column_config={
                    'Column name': st.column_config.TextColumn(
                        help='Name of the column',
                        width = 'large',
                        required=True
                    ),
                    "Data type": st.column_config.SelectboxColumn(
                        help="The category of the app",
                        width="medium",
                        options=[
                            "Numbers 🎲",
                            "Categories 🚦",
                            "Dates 🗓",
                        ],
                        required=True
                    )
                },
                hide_index=False,
                key = state['editor_key_datatypes']
            )

            # Choosing action #
            cols = st.columns(3)
            with cols[0] :
                reset_changes = st.button(label='Reset changes')
            with cols[1] :
                submit_changes = st.button(label='Submit changes')

            # Resetting the changes #
            if reset_changes :
                state['editor_key_datatypes'] += 1
                st.rerun()

            # Submitting the edited changes #
            if submit_changes :
                # Renaming columns #
                new_colnames_mp = {}
                for i in col_types_df.index :
                    new_colnames_mp[ col_types_df['Column name'][i] ] = edited_df['Column name'][i]

                state['preprocessed_df'].rename( new_colnames_mp, axis=1, inplace=True )

                # Changing Data Types #
                convert_mp = {'Numbers 🎲':'int64', 'Categories 🚦':'object', 'Dates 🗓':'datetime64'}
                new_datatypes_mp = {}
                for i in edited_df.index :
                    new_datatypes_mp[ edited_df['Column name'][i] ] = convert_mp[ edited_df['Data type'][i] ]

                # st.write(new_datatypes_mp)
                for col, new_type in new_datatypes_mp.items() :
                    if state['preprocessed_df'][col].dtype not in ['int64','float64'] and new_type == 'int64' :
                        state['preprocessed_df'][col] = state['preprocessed_df'][col].astype('int64')

                    elif state['preprocessed_df'][col].dtype not in ['object'] and new_type == 'object' :
                        state['preprocessed_df'][col] = state['preprocessed_df'][col].astype('str')

                    elif state['preprocessed_df'][col].dtype not in ['datetime64', 'datetime64[ns]'] and new_type == 'datetime64' :
                        state['preprocessed_df'][col] = state['preprocessed_df'][col].astype('datetime64')


                st.success('Successfully changed data types!')
                time.sleep(1.5)
                st.rerun()

    ##################################################################################################
    def set_base_date_col(self) -> None :
        #############################
        # Choosing base date column #
        #############################
        with st.expander('Setting base date column') :
            # Finding all the date columns #
            date_col_options = []
            for col in state['preprocessed_df'].columns :
                if state['preprocessed_df'][col].dtype in ['datetime64','datetime64[ns]'] :
                    date_col_options.append(col)

            # Asking for the base date choice #
            base_param_choice = st.selectbox(
                label='Choose one of the dates to be your base date',
                options=date_col_options
            )

            # Submit the choice #
            submit_basedate_choice = st.button(label='Submit base date choice')

            if submit_basedate_choice:
                state['base_date'] = base_param_choice
                st.success(f'{base_param_choice} is set as your base date column!')
                time.sleep(1.5)
                st.rerun()


########################################################################################################################
########################################################################################################################
def show_preprocessed() -> None :
    # Checking for the existance of data #
    if 'preprocessed_df' not in state :
        st.warning('Please upload a Dataset first')
        st.stop()

    #####################################
    # Showing the new preprocessed data #
    #####################################
    st.subheader(':rainbow[Preprocessed data:]')
    st.write(state['preprocessed_df'].head(200))

    ####################################################
    # Showing the general info about the preprocessing #
    ####################################################
    if 'base_date' in state :
        hr()
        base_date = state['base_date']
        st.info(f'Base date column: {base_date}')

    #####################################
    # Displaying shape and column types #
    #####################################
    cols = st.columns(2)
    with cols[0] :
        st.info( f"Dataset contains: :green[{state['preprocessed_df'].shape[0]}] rows and :green[{state['preprocessed_df'].shape[1]}] columns" )
        total_cells = state['preprocessed_df'].shape[0]*state['preprocessed_df'].shape[1]
        total_nans = state['preprocessed_df'].isna().sum().sum()
        nans_percent = round(total_nans/total_cells*100,1)

    with cols[1] :
        st.info( f"In total :green[{total_cells}] cells, where :green[{total_nans}] (:green[{nans_percent}%]) are empty" )

    ####################
    # Data description #
    ####################
    hr()
    st.subheader('Data description:')

    st.write('Numeric Columns:')
    st.dataframe( state['preprocessed_df'].describe().drop(['25%','50%','75%']).T, use_container_width=True)

    st.write('Categorical Columns:')
    st.dataframe( state['preprocessed_df'].describe(include='object').T, use_container_width=True )


    hr()
    cols = st.columns(4)

    #################################
    # Download preprocessed dataset #
    #################################
    with cols[0] :
        with st.expander('Download Preprocessed Data') :
            download_choice = st.radio(label='Choose Extension', options=['Excel', 'CSV'], horizontal=True)
            
            if download_choice == 'CSV' :
                download_button = st.download_button(
                    label="Download data as CSV",
                    data=state['preprocessed_df'].to_csv().encode('utf-8'),
                    file_name='preprocessed_df.csv',
                    mime='text/csv',
                )
            elif download_choice == 'Excel' :
                buffer = io.BytesIO()

                with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
                    # Write each dataframe to a different worksheet.
                    df = state['preprocessed_df'].copy()
                    df.to_excel(writer, sheet_name='Sheet1', index=False)

                    download_button = st.download_button(
                        label="Download data as Excel",
                        data=buffer,
                        file_name='large_df.xlsx',
                        mime='application/vnd.ms-excel'
                    )


    ###########################
    # Reset preprocessed data #
    ###########################
    with cols[1] :
        reset_preprocessed_button = st.button('Reset Preprocessed Data')

    if reset_preprocessed_button :
        state['preprocessed_df'] = state['original_df'].copy()
        st.success('Successfully reseted Preprocessing settings!')
        time.sleep(1.5)
        st.rerun()



    # # Showing data types #
    # space(2)
    # num_cols, cat_cols, date_cols = [], [], []
    # for col in state['preprocessed_df'].columns :
    #     if state['preprocessed_df'][col].dtype in ['int','float'] :
    #         num_cols.append(col)
    #     elif state['preprocessed_df'][col].dtype in ['str', 'object'] :
    #         cat_cols.append(col)
    #     elif state['preprocessed_df'][col].dtype in ['datetime64','datetime64[ns]'] :
    #         date_cols.append(col)

    # # Find the maximum length among the arrays
    # max_length = max(len(num_cols), len(cat_cols), len(date_cols))

    # # Create series of equal length with NaN values where necessary
    # num_series = pd.Series(num_cols + [np.nan] * (max_length - len(num_cols)))
    # cat_series = pd.Series(cat_cols + [np.nan] * (max_length - len(cat_cols)))
    # date_series = pd.Series(date_cols + [np.nan] * (max_length - len(date_cols)))

    # # Create the DataFrame
    # cols_view_df = pd.DataFrame(data={
    #     'Numerical': num_series,
    #     'Categorical': cat_series,
    #     'Date&Time': date_series
    # })
    
    # st.subheader('Column types:')
    # st.dataframe(cols_view_df, use_container_width=True,hide_index=True)