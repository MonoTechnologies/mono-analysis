import pandas as pd
import time

import streamlit as st
from streamlit import session_state as state
from streamlit_option_menu import option_menu
from streamlit_extras.dataframe_explorer import dataframe_explorer

# from pydantic_settings import BaseSettings
# from pandas_profiling import ProfileReport
# from streamlit_pandas_profiling import st_profile_report

import matplotlib.pyplot as plt
import altair as alt

from utils import *

################################################################
################################################################
def start() -> None :
	st.markdown("<h1 style='text-align: center;'>Data Analysis</h1>", unsafe_allow_html=True)

	# Choosing analysis type #
	analysis_button = option_menu(
		menu_title = None,
		options = ["General", "Manual charting", 'Deep analytics', 'AI assistant'],
		icons = ['bar-chart-fill', 'search','body-text' ,'robot', 'gear'],
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
	elif analysis_button == 'Manual charting' :
		Manual_analysis()
	# elif analysis_button == 'Deep analytics' :
	# 	perform_pandas_profiling()
	

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
                #############################
                # Input -> features to plot #
                hr()
                self.chart_features = self.input_chart_features()
                
                #######################
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
        
        ####################################
        # Reordering features by Data Type #
        ordered_chart_features = []
        for col in chart_features :
            if state['preprocessed_df'][col].dtype in ['int','float', 'int64', 'float64'] :
                ordered_chart_features.append(col)
        
        for col in chart_features :
            if state['preprocessed_df'][col].dtype in ['str', 'object'] :
                ordered_chart_features.append(col)

        for col in chart_features :
            if state['preprocessed_df'][col].dtype in ['datetime64','datetime64[ns]'] :
                ordered_chart_features.append(col)


        return ordered_chart_features
    

    ####################################################################################
    def input_chart_type(self) -> str :
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
            possible_chart_options = ['Scatter Plot', 'Mean Bars']
        
        elif numeric_cols == 0 and categorical_cols == 2 and date_cols == 0 :
            possible_chart_options = ['Stacked Bar Chart']

        elif numeric_cols == 1 and categorical_cols == 1 and date_cols == 0 :
            possible_chart_options = ['Grouped Box Plot']
        
        elif numeric_cols == 1 and categorical_cols == 0 and date_cols == 1 :
            possible_chart_options = ['History Line']

        elif numeric_cols == 0 and categorical_cols == 1 and date_cols == 1 :
            possible_chart_options = ['History Bars']
        
        elif numeric_cols == 2 and categorical_cols == 1 and date_cols == 0 :
            possible_chart_options = ['Colored Scatter Plot']

        elif numeric_cols == 1 and categorical_cols == 1 and date_cols == 1 :
            possible_chart_options = ['Grouped History Line']

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
        with st.columns(4)[0] :
            chart_type = st.selectbox(
                label = 'Chart type:',
                options = possible_chart_options,
                key = 'select_chart'+str(self.current_view)
            )
        
        return chart_type
    

    ####################################################################################
    def view_buttons(self) -> None :
        ######################
        # Generating a chart #
        cols = st.columns(6)
        with cols[0] :
            generate_plot = st.button('Generate a chart', key = 'generate'+str(self.current_view))

        if generate_plot:
            Plot_figure(
                features = list(self.chart_features),
                chart_type = self.chart_type
            )

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



################################################################
################################################################
class Plot_figure :
    def __init__(self, features: list, chart_type: str ) -> None :
        self.features = features

        if chart_type == 'Histogram' :
            self.plot_histogram()
        elif chart_type == 'Scatter Plot' :
            self.plot_scatter()
        elif chart_type == 'Bar Chart' :
            self.plot_barchart()
        elif chart_type == 'Mean Bars' :
            self.plot_mean_bars()
        elif chart_type == 'Pie Chart' :
            self.plot_piechart()
        elif chart_type == 'Box Plot' or chart_type == 'Grouped Box Plot' :
            self.plot_boxplot()
        elif chart_type == 'Stacked Bar Chart' :
            self.plot_stacked_barchart()
        elif chart_type == 'History Line' :
            self.plot_history_line()
        elif chart_type == 'History Bars' :
            self.plot_history_bars()
        elif chart_type == 'Colored Scatter Plot' :
            self.plot_colored_scatter()
        elif chart_type == 'Grouped History Line' :
            self.plot_grouped_history_line()

    #######################################################
    def plot_histogram(self) -> None :
        alt_chart = alt.Chart( state['preprocessed_df'] ).mark_bar().encode(
            alt.X(self.features[0]),
            y='count()',
        )
        st.altair_chart(alt_chart, theme=None, use_container_width=True)

    #######################################################
    def plot_scatter(self) -> None :
        st.scatter_chart(
            state['preprocessed_df'],
            x = self.features[0],
            y = self.features[1]
            # color='col4',
            # size='col3',
        )

    #######################################################
    def plot_mean_bars(self) -> None :
        if len(self.features) == 2 :
            grouped_data = state['preprocessed_df'].groupby(self.features[0])[self.features[1]].mean().reset_index()

            alt_chart = alt.Chart(grouped_data).mark_bar().encode(
                alt.X(self.features[0]),
                alt.Y(self.features[1], title='Mean of '+self.features[1]),
            )

        st.altair_chart(alt_chart, theme=None, use_container_width=True)

    #######################################################
    def plot_boxplot(self) -> None:
        if len(self.features) == 1 :
            alt_chart = alt.Chart( state['preprocessed_df'] ).mark_boxplot().encode(
                alt.X(self.features[0]+":Q")
            )
        elif len(self.features) == 2 :
            alt_chart = alt.Chart( state['preprocessed_df'] ).mark_boxplot().encode(
                alt.X(self.features[0]+':Q'),
                alt.Y(self.features[1]+':N')
            )
        st.altair_chart(alt_chart, theme=None, use_container_width=True)

    #######################################################
    def plot_barchart(self) -> None :
        alt_chart = alt.Chart( state['preprocessed_df'] ).mark_bar().encode(
            alt.X( self.features[0] ),
            alt.Y( 'count()' )
        )
        st.altair_chart(alt_chart, theme=None, use_container_width=True)

    #######################################################
    def plot_piechart(self) -> None :
        # Calculate value counts for self.features[0]
        value_counts = state['preprocessed_df'][self.features[0]].value_counts().reset_index()

        chart = alt.Chart(value_counts).mark_arc().encode(
            color=alt.Color(field=self.features[0], type="nominal", title='Class:'),
            theta=alt.Theta(field='count', type="quantitative", title='Frequency:')
        )
        st.altair_chart(chart, use_container_width=True)

    #######################################################
    def plot_stacked_barchart(self) -> None :
        chart = alt.Chart( state['preprocessed_df'] ).mark_bar().encode(
            alt.X(self.features[0]),
            alt.Y( f'count({self.features[1]})', title='Count' ),
            color = self.features[1]
        )
        st.altair_chart(chart, use_container_width=True)
    
    ########################################################
    def plot_history_line(self) -> None :

        custom_df = state['preprocessed_df'].copy()

        custom_df['year'] = custom_df[self.features[1]].dt.year
        custom_df['month'] = custom_df[self.features[1]].dt.month

        # Group by year and month, calculate the mean of 'numeric_column'
        monthly_mean_df = custom_df.groupby(['year', 'month'])[self.features[0]].mean().reset_index()

        # Combine year and month into a single datetime column for plotting
        monthly_mean_df['date'] = pd.to_datetime(monthly_mean_df[['year', 'month']].assign(day=1))

        chart = alt.Chart(monthly_mean_df).mark_bar().encode(
            x=alt.X('date:T', title='Month'),
            y= f'mean({self.features[0]}):Q'
        )
        st.altair_chart(chart, use_container_width=True)

    ########################################################
    def plot_history_bars(self) -> None :
        custom_df = state['preprocessed_df'].copy()

        custom_df['year'] = custom_df[self.features[1]].dt.year
        custom_df['month'] = custom_df[self.features[1]].dt.month

        monthly_category_counts_df = custom_df.groupby(['year', 'month', self.features[0] ]).size().reset_index(name='count')

        monthly_category_counts_df['date'] = pd.to_datetime(monthly_category_counts_df[['year', 'month']].assign(day=1))

        # Create Altair chart
        chart = alt.Chart(monthly_category_counts_df).mark_bar().encode(
            x=alt.X('date:T', title='Month'),
            y=alt.Y('count:Q', title='Count'),
            color=alt.Color(self.features[0] + ':N', title='Category')
        )
        st.altair_chart(chart, use_container_width=True)
    ########################################################
    def plot_colored_scatter(self) :
        chart = alt.Chart( state['preprocessed_df'] ).mark_circle(size=60).encode(
            x = self.features[0],
            y = self.features[1],
            color = self.features[2],
            # tooltip=['Name', 'Origin', 'Horsepower', 'Miles_per_Gallon']
        ).interactive()
        st.altair_chart(chart, use_container_width=True)
    ########################################################
    def plot_grouped_history_line(self) :
        custom_df = state['preprocessed_df'].copy()

        custom_df['year'] = custom_df[self.features[2]].dt.year
        custom_df['month'] = custom_df[self.features[2]].dt.month

        monthly_mean_df = custom_df.groupby(['year', 'month', self.features[1]])[self.features[0]].mean().reset_index()

        monthly_mean_df['date'] = pd.to_datetime(monthly_mean_df[['year', 'month']].assign(day=1))

            
        highlight = alt.selection(type='single', on='mouseover',
                                fields=['symbol'], nearest=True)

        base = alt.Chart( monthly_mean_df ).encode(
            x='date:T',
            y=alt.Y(f'{self.features[0]}:Q', title = f'Mean of {self.features[0]}'),
            color=f'{self.features[1]}:N'
        )

        points = base.mark_circle().encode( opacity=alt.value(0) ).add_selection( highlight ).properties( width=600 )

        lines = base.mark_line().encode(
            size=alt.condition(~highlight, alt.value(1), alt.value(3))
        )

        alt_chart = points + lines

        st.altair_chart(alt_chart, theme="streamlit", use_container_width=True)

