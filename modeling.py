import streamlit as st
from streamlit import session_state as state

from utils import *

def start() -> None :
    st.markdown("<h1 style='text-align: center;'>Predictors</h1>", unsafe_allow_html=True)
    hr()

    # Checking if we uploaded a df #
    if 'preprocessed_df' not in state :
        st.info('Please upload a Dataset first')
        st.stop()

    # Showing the current stage #
    if state['modeling_stage'] == 0 :
        prediction_type()
    elif state['modeling_stage'] == 1:
        choosing_target()
    elif state['modeling_stage'] == 2:
        fitting_model()
    elif state['modeling_stage'] == 3 :
        show_matrics()
    elif state['modeling_stage'] == 4 :
        final_stage()
    

##########################################################################################################################
def prediction_type() -> None :
    st.markdown("<h3 style='text-align: center;'> Step 1/5: Choose prediction method: </h3>", unsafe_allow_html=True)

    ################################
    # Choosing which method to use #
    cols = st.columns(3)
    with cols[1] :
        model_type = st.radio('',['Classification', 'Regression', 'Time Seeries'])

    state['model_type'] = model_type

    ###########################
    # A tip about model types #
    if model_type == 'Classification' :
        st.info('Classification: Predicting a class. For instance: the borrower is legit, or it is better to not issue a loan.')
    elif model_type == 'Regression' :
        st.info('Regression: Predicing a number. For instance: the cost of the car should be X Somoni, or the area of this house must be around X squared metres.')
    else:
        st.info('Time Series: Predicting a value based on the given date. For instance: The stock will be around X dollars on jan 1, 2026.')

    ########################
    # Showing step buttons #
    space(7)
    cols = st.columns(5)
    with cols[0] :
        prev_button = st.button('<< Previous', disabled = True)
    with cols[4] :
        next_button = st.button('Next >>')

    ############################
    # Changing stage if needed #
    if next_button :
        state['modeling_stage'] += 1
        st.rerun()



##########################################################################################################################
def choosing_target() -> None :
    st.markdown("<h3 style='text-align: center;'> Step 2/5: Choose a column to predict: </h3>", unsafe_allow_html=True)

    ############################
    # Choosing a target column #
    target = st.selectbox('', state['preprocessed_df'].columns, index=20)
    state['target'] = target

    # Checking whether model type and target type are correct #
    target_type = state['preprocessed_df'][target].dtype
    
    ########################
    # Showing step buttons #
    space(7)
    cols = st.columns(5)
    with cols[0] :
        prev_button = st.button('<< Previous')
    with cols[4] :
        next_button = st.button('Next >>', disabled = False)

    ############################
    # Changing stage if needed #
    if next_button :
        state['modeling_stage'] += 1
        st.rerun()
    elif prev_button :
        state['modeling_stage'] -= 1
        st.rerun()

##########################################################################################################################
def fitting_model() -> None :
    st.markdown("<h3 style='text-align: center;'> Step 3/5: Training an AI: </h3>", unsafe_allow_html=True)

    ################
    # Fake loading #

    if 'trained_model' not in state :
        state['trained_model'] = True
        training_epoch = st.progress(0, text='Training a model, this might take a while...')
        
        for i in range(101) :
            if i == 100 :
                text = ':green[Training finished!]'
            elif i > 75 :
                text = ':pink[Almost there.....]'
            else :
                text = 'Training a model, this might take a while...'
            training_epoch.progress(i, text=f'{text}')
            time.sleep(0.1)
    
    else :
        training_epoch = st.progress(0, text='Training a model, this might take a while...')
        training_epoch.progress(100, text=f':green[Training finished!]')


    ########################
    # Showing step buttons #
    space(7)
    cols = st.columns(5)
    with cols[0] :
        prev_button = st.button('<< Previous')
    with cols[4] :
        next_button = st.button('Next >>', disabled = False)

    ############################
    # Changing stage if needed #
    if next_button :
        state['modeling_stage'] += 1
        st.rerun()
    elif prev_button :
        state['modeling_stage'] -= 1
        st.rerun()


##########################################################################################################################
def show_matrics() -> None :
    st.markdown("<h3 style='text-align: center;'> Step 4/5: Evaluating metrics: </h3>", unsafe_allow_html=True)
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
    space(7)
    cols = st.columns(5)
    with cols[0] :
        prev_button = st.button('<< Previous')
    with cols[4] :
        next_button = st.button('Next >>', disabled = False)

    ############################
    # Changing stage if needed #
    if next_button :
        state['modeling_stage'] += 1
        st.rerun()
    elif prev_button :
        state['modeling_stage'] -= 1
        st.rerun()

##########################################################################################################################
def final_stage() -> None :
    st.markdown("<h3 style='text-align: center;'> Step 5/5: Final stage: </h3>", unsafe_allow_html=True)
    space(3)

    st.markdown("<h4 style='text-align: center;'>Congrats on deploying your first model! </h4>", unsafe_allow_html=True)
    st.balloons()


    ########################
    # Showing step buttons #
    space(7)
    cols = st.columns(5)
    with cols[0] :
        prev_button = st.button('<< Previous')
    with cols[4] :
        next_button = st.button('Next >>', disabled = True)

    ############################
    # Changing stage if needed #
    if next_button :
        state['modeling_stage'] += 1
        st.rerun()
    elif prev_button :
        state['modeling_stage'] -= 1
        st.rerun()