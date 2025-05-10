import streamlit as st
from streamlit import session_state as state
from sklearn.model_selection import train_test_split

from utils import *



def show_step_buttons() :
    cols = st.columns(5)
    with cols[0] :
        if state['modeling_stage'] == 0 :
            disabled_button = True
        else: disabled_button = False

        prev_button = st.button('<< Previous', disabled = disabled_button)

    with cols[4] :
        if state['modeling_stage'] == 5 :
            disabled_button = True
        else: disabled_button = False

        next_button = st.button('Next >>', disabled = disabled_button)

    ############################
    # Changing stage if needed #
    ############################
    if next_button :
        state['modeling_stage'] += 1
        st.rerun()
    elif prev_button :
        state['modeling_stage'] -= 1;
        st.rerun()



def start() -> None :
    st.markdown("<h1 style='text-align: center;'>Predictors</h1>", unsafe_allow_html=True)
    hr()

    # Checking if we uploaded a df #
    if 'preprocessed_df' not in state :
        st.info('Please upload a Dataset first')
        st.stop()

    # Warning if we don't have enough observations #
    if state['preprocessed_df'].shape[0] < 200:
        st.warning(f"WARNING!\n You only have {state['preprocessed_df'].shape[0]} rows which may not be enough to train a good model :(")

    #############################
    # Showing the current stage #
    #############################
    if state['modeling_stage'] == 0 :
        prediction_method()
    elif state['modeling_stage'] == 1:
        choosing_target()
    elif state['modeling_stage'] == 2:
        select_columns()
    elif state['modeling_stage'] == 3:
        training_process()
    elif state['modeling_stage'] == 4:
        show_matrics()
    elif state['modeling_stage'] == 5:
        final_stage()
    

##########################################################################################################################
def prediction_method() -> None :
    st.markdown("<h3 style='text-align: center;'> Step 1/6: Choose prediction method: </h3>", unsafe_allow_html=True)

    ################################
    # Choosing which method to use #
    ################################
    cols = st.columns(3)
    with cols[1] :
        prediction_method = st.radio('',['Classification', 'Regression', 'Forecast'])

    state['prediction_method'] = prediction_method

    ###########################
    # A tip about model types #
    ###########################
    if prediction_method == 'Classification' :
        st.info('Classification: Predicting a class. For instance: the borrower is legit, or it is better to not issue a loan.')
    elif prediction_method == 'Regression' :
        st.info('Regression: Predicing a number. For instance: the cost of the car should be X Somoni, or the area of this house must be around X squared metres.')
    else:
        st.info('Forecasting: Predicting a value based on the given date. For instance: The stock will be around X dollars on jan 1, 2026.')


    #######################################
    # Checking if we are ready to proceed #
    #######################################
    space(7)
    show_step_buttons()



##########################################################################################################################
def choosing_target() -> None :
    st.markdown("<h3 style='text-align: center;'> Step 2/6: Choose a column to predict: </h3>", unsafe_allow_html=True)

    # Choosing a target column #
    target = st.selectbox('', state['preprocessed_df'].columns, index=20)
    state['prediction_target'] = target

    # Checking whether model type and target type are correct #
    target_type = state['preprocessed_df'][target].dtype
    st.write(target_type)

    if state['prediction_method'] == 'Classification' :
        if 'date' in str(target_type) :
            st.error('You cannot use a Date type column in Classification method! Please choose Forecast method for DateType columns.')

    if state['prediction_method'] == 'Regression' :
        if 'obj' in str(target_type) or 'date' in str(target_type) :
            st.error('Categorical and Date columns cannot be used in Regression method! Please change prediction method or the column!')

    if state['prediction_method'] == 'Forecast' :
        if 'date' not in str(target_type) :
            st.error('The given column is not a Date column! Please change prediction method or the column!')

    
    ########################
    # Showing step buttons #
    ########################
    space(7)
    show_step_buttons()


##########################################################################################################################
def select_columns() -> None:
    st.markdown("<h3 style='text-align: center;'> Step 3/6: Select useful columns for prediction: </h3>", unsafe_allow_html=True)
    
    # Selecting columns #
    default_columns = [
        col for col in state['preprocessed_df'].columns 
        if "date" not in str(state['preprocessed_df'][col].dtype).lower()
    ]

    selected = st.multiselect(
        label = 'Selected columns:',
        options = state['preprocessed_df'].columns,
        default = default_columns
    )
    state['training_columns'] = selected

    ########################
    # Showing step buttons #
    ########################
    space(7)
    show_step_buttons()


##########################################################################################################################
def fill_df_nans(df) -> pd.DataFrame() :
    df_filled = df.copy()

    # Identify numeric and categorical columns
    numeric_columns = df_filled.select_dtypes(include=['number']).columns
    categorical_columns = df_filled.select_dtypes(exclude=['number']).columns
    
    # Fill numeric columns with their mean values
    for col in numeric_columns:
        mean_value = df_filled[col].mean()
        df_filled[col] = df_filled[col].fillna(mean_value)
    
    # Fill categorical columns with "Null Value"
    for col in categorical_columns:
        df_filled[col] = df_filled[col].fillna("Null Value")

    return df_filled.copy()


def transform_cat_columns(df) -> pd.DataFrame():
    new_df = df.copy()
    categorical_columns = new_df.select_dtypes(include=['object']).columns

    for col in categorical_columns :
        dummy = pd.get_dummies(new_df[col], prefix=col)
        new_df.drop(col, axis=1, inplace=True)
        new_df = pd.concat([new_df, dummy], axis=1)

    return new_df


class training_process() :
    def __init__(self) -> None:
        st.markdown("<h3 style='text-align: center;'> Step 4/6: Training an AI model: </h3>", unsafe_allow_html=True)

        self.preprocess_data()
        self.fit_model()

        # Showing step buttons #
        space(7)
        show_step_buttons()


    def preprocess_data(self) -> None:
        # Filling up NaN values #
        state['train_df'] = fill_df_nans( state['preprocessed_df'] )

        # Transforming variables #
        state['train_df'] = transform_cat_columns( state['train_df'] )


    def fit_model(self) -> None :

        state['train_df'], state['test_df'] = train_test_split(
            state['train_df'],
            test_size = 0.2,
            random_state = 42
        )
        st.write(state['train_df'])
        st.write(state['test_df'])


        # # Fake loading #
        # if 'trained_model' not in state :
        #     state['trained_model'] = True
        #     training_epoch = st.progress(0, text='Training a model, this might take a while...')
            
        #     for i in range(101) :
        #         if i == 100 :
        #             text = ':green[Training finished!]'
        #         elif i > 75 :
        #             text = ':pink[Almost there.....]'
        #         else :
        #             text = 'Training a model, this might take a while...'
        #         training_epoch.progress(i, text=f'{text}')
        #         time.sleep(0.01)
        
        # else :
        #     training_epoch = st.progress(0, text='Training a model, this might take a while...')
        #     training_epoch.progress(100, text=f':green[Training finished!]')


    


##########################################################################################################################
def show_matrics() -> None :
    st.markdown("<h3 style='text-align: center;'> Step 5/6: Evaluating metrics: </h3>", unsafe_allow_html=True)
    space(3)

    cols = st.columns(3)

    with cols[0] :
        st.metric('Total Accuracy',value=f'{75}%')

    with cols[1] :
        st.metric('Positives(1) found',value=f'{78}%')
    
    with cols[2] :
        st.metric('Negatives(0) found',value=f'{71}%')


    ########################
    # Showing step buttons #
    ########################
    space(7)
    show_step_buttons()



##########################################################################################################################
def final_stage() -> None :
    st.markdown("<h3 style='text-align: center;'> Step 6/6: Final stage: </h3>", unsafe_allow_html=True)
    space(3)

    st.markdown("<h4 style='text-align: center;'>Congrats on deploying your first model! </h4>", unsafe_allow_html=True)
    st.balloons()


    ########################
    # Showing step buttons #
    ########################
    space(7)
    show_step_buttons()