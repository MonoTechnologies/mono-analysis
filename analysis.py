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
def start() -> None :
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
		General_analysis()
	elif analysis_button == 'Manual charts' :
		Manual_analysis()
	elif analysis_button == 'Pandas Profiling' :
		perform_pandas_profiling()
	

################################################################
################################################################
class General_analysis :
    ####################################################################################
    def __init__(self) -> None :

        # Calculate the shape and column structure #
        self.calculate_metrics()

        # Show general data descripton #
        self.display_column_info()

    ####################################################################################
    def calculate_metrics(self) :
        st.subheader('Overview of the Preprocessed Dataset')
        st.dataframe(state['preprocessed_df'].head(200), use_container_width=True)

        ##############################
        # Shwoing the number of rows #
        cols = st.columns(5)

        with cols[1] :
            st.metric(
                label='Number of rows',
                value=state['preprocessed_df'].shape[0],
                delta=state['preprocessed_df'].shape[0] - state['original_df'].shape[0],
                delta_color='off'
            )
        #################################
        # Showing the number of columns #
        with cols[2] :
            st.metric(
                label='Number of columns',
                value=state['preprocessed_df'].shape[1],
                delta=state['preprocessed_df'].shape[1] - state['original_df'].shape[1],
                delta_color='off'
            )
        ####################################
        # Showing the numbr of empty cells #
        total_cells = state['preprocessed_df'].shape[0]*state['preprocessed_df'].shape[1]
        total_nans = state['preprocessed_df'].isna().sum().sum()
        nans_percent = round(total_nans/total_cells*100,1)
        with cols[3] :
            st.metric(
                label='Empty cells',
                value=state['preprocessed_df'].isna().sum().sum(),
                delta=str(nans_percent)+'%',
                delta_color= 'off' if nans_percent < 10 else 'inverse'
            )

    ####################################################################################
    def display_column_info(self) :
        ########################
        # Showing Column types # 
        hr()
        st.subheader('Column types:')

        ##############################################
        num_cols, cat_cols, date_cols = [], [], []
        for col in state['preprocessed_df'].columns :
            if state['preprocessed_df'][col].dtype in ['int','float'] :
                num_cols.append(col)
            elif state['preprocessed_df'][col].dtype in ['str', 'object'] :
                cat_cols.append(col)
            elif state['preprocessed_df'][col].dtype in ['datetime64','datetime64[ns]'] :
                date_cols.append(col)

        cols = st.columns(5)
        with cols[1] :
            st.metric(
                label='Numeric columns',
                value=len(num_cols),
            )
        with cols[2] :
            st.metric(
                label='Categorical columns',
                value=len(cat_cols)
            )
        with cols[3] :
            st.metric(
                label='Date&Time columns',
                value=len(date_cols)
            )

        ##############################
        # Showing columns themselves #
        st.table( state['preprocessed_df'].dtypes )

        ####################
        # Data description #
        hr()
        st.subheader('Data description:')

        st.write('Numeric Columns:')
        st.dataframe( state['preprocessed_df'].describe().drop(['25%','50%','75%']).T, use_container_width=True)

        st.write('Categorical Columns:')
        st.dataframe( state['preprocessed_df'].describe(include='object').T, use_container_width=True )

        # Null values #
        hr()
        st.subheader('Null values (Empty cells)')
        st.table( state['preprocessed_df'].isna().sum() )



################################################################
################################################################
def perform_pandas_profiling() -> None :
	st.info('Pandas Profiling is a detailed explanation of your Data. Thus it can take some time to generate.')
	generate_profiling_button = st.button('Generate Pandas Profiling')

	if generate_profiling_button :
		pr = state['preprocessed_df'].profile_report()
		st_profile_report(pr)


################################################################
################################################################
class Manual_analysis :
    ####################################################################################
    def __init__(self) :
        """
        Chart views -> Tuple -> (View's Num, Type of Chart, Column Name(s) for chart)
        """
        ###########################
        # Adding a new chart-view #
        self.add_view()

        ##################################
        # Showing all the View expanders #
        for chart_view in state['chart_views'] :
            self.current_view = chart_view[0]
            
            with st.expander( f"Chart view Num. {self.current_view}", expanded=False ) :
                ###########################
                # Input -> features to plot #
                hr()
                self.chart_features = self.input_chart_features()
                
                #####################
                # Input -> chart type #
                hr()
                self.chart_type = self.input_chart_type()
                
                ######################
                # Generating buttons #
                hr()
                self.view_buttons()


    ####################################################################################
    def add_view( self ) -> None :
        '''
        A sub-function for adding a new view
        '''
        new_view = st.button('➕ Add a view')
        space(2)
        if new_view :
            state['chart_views'].append( ( len(state['chart_views'])+1, None, [] ) )


    ####################################################################################
    def input_chart_features( self ) -> list :
        '''
        A sub-function to input column names to plot
        '''

        #########################################
        # Asking the number of features to plot #
        feature_nums = st.radio(
            label='Choose the number of columns for the chart',
            options=['One column', 'Two columns', 'Three columns'],
            horizontal=True,
            key=self.current_view
        )
        ###################################
        # Asking for the features to plot #
        chart_features = []
        feat_cols = st.columns(3)

        if feature_nums in ['One column','Two columns', 'Three columns'] :
            with feat_cols[0] :
                col1 = st.selectbox('Column 1',options=state['preprocessed_df'].columns, key='col_1'+str(self.current_view) )
                chart_features.append(col1)
        
        if feature_nums in ['Two columns','Three columns'] :
            with feat_cols[1] :
                col2 = st.selectbox('Column 2',options=state['preprocessed_df'].columns, key='col_2'+str(self.current_view) )
                chart_features.append(col2)
            
        if feature_nums == 'Three columns' :
            with feat_cols[2] :
                col3 = st.selectbox('Column 3',options=state['preprocessed_df'].columns, key='col_3'+str(self.current_view) )
                chart_features.append(col3)
            
        return chart_features
    

    ####################################################################################
    def input_chart_type(self) :
        '''
        A sub-function for selecting chart type
        '''

        #######################################
        # Finding data types of chart columns #
        numeric_cols, categorical_cols, date_cols = 0,0,0
        for col in self.chart_features :
            if state['preprocessed_df'][col].dtype in ['int','float', 'int64', 'float64'] :
                numeric_cols += 1
            elif state['preprocessed_df'][col].dtype in ['str', 'object'] :
                categorical_cols += 1
            elif state['preprocessed_df'][col].dtype in ['datetime64','datetime64[ns]'] :
                date_cols += 1
        
        ##############################################################
        # Selecting possible chart options based on column datatypes #
        if numeric_cols == 1 and categorical_cols == 0 and date_cols == 0:
            possible_chart_options = [ 'Histogram', 'Box Plot' ]
        
        elif numeric_cols == 0 and categorical_cols == 1 and date_cols == 0 :
            possible_chart_options = ['Bar Chart', 'Pie Chart']

        elif numeric_cols == 2 and categorical_cols == 0 and date_cols == 0 :
            possible_chart_options = ['Scatter Plot']
        
        elif numeric_cols == 0 and categorical_cols == 2 and date_cols == 0 :
            possible_chart_options = ['Stacked Bar Chart']

        #####################################
        # Invalid Column types for plotting #
        else :
            if numeric_cols and categorical_cols and date_cols :
                st.warning( f'Sorry, currently we do not provide charts with {numeric_cols} Numeric, {categorical_cols} Categorical, and {date_cols} DateTime features' )
            elif numeric_cols and categorical_cols:
                st.warning( f'Sorry, currently we do not provide charts with {numeric_cols} Numeric, {categorical_cols} Categorical features' )
            elif numeric_cols and date_cols :
                st.warning( f'Sorry, currently we do not provide charts with {numeric_cols} Numeric and {date_cols} DateTime features' )
            elif categorical_cols and date_cols :
                st.warning( f'Sorry, currently we do not provide charts with {categorical_cols} Categorical and {date_cols} DateTime features' )
            elif numeric_cols :
                st.warning( f'Sorry, currently we do not provide charts with {numeric_cols} Numeric features' )
            elif categorical_cols :
                st.warning( f'Sorry, currently we do not provide charts with {categorical_cols} Categorical features' )
            elif date_cols :
                st.warning( f'Sorry, currently we do not provide charts with {date_cols} DateTime features' )
            
            st.stop()

        ################################
        # input -> Choosing chart type #
        with st.columns(5)[0] :
            chart_type = st.selectbox(
                label = 'Chart type:',
                options = possible_chart_options,
                key = 'select_chart'+str(self.current_view)
            )
        
        return chart_type
    

    ####################################################################################
    def view_buttons(self) :
        ######################
        # Generating a chart #
        cols = st.columns(6)
        with cols[0] :
            st.button('Generate a chart', key = 'generate'+str(self.current_view))

        ###################
        # Deleting a view #
        with cols[1] :
            delete_view = st.button('Delete view', key='delete'+str(self.current_view))
        if delete_view :
            # Deleting the current view #
            del_pos = self.current_view-1
            del state['chart_views'][del_pos]

            # Resetting chart_views indexes #
            for i in range( len(state['chart_views']) ) :
                state['chart_views'][i] = (i+1, state['chart_views'][i][1], state['chart_views'][i][2] )

            st.rerun()