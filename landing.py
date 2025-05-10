import streamlit as st
from streamlit import session_state as state

from utils import *

###########################################################################################

def start() :
    wiki()
    hr()
    quick_example()
    
###########################################################################################
def wiki() :
    # Some winter vibes #
    # st.snow()

    # Showing the title #
    st.title("💬 Mono-AI")
    hr()
    
    # Define the CSS styling for the rectangle
    style = """
        <style>
            .rectangle {
                border: 1px solid #fff;
                padding: 20px;
                border-radius: 20px;
            }
        </style>
    """
    # Display the styled text inside the rectangle
    st.markdown(style, unsafe_allow_html=True)
    # st.write(f'<div class="rectangle">{text}</div>', unsafe_allow_html=True)
    
    columns = st.columns(4)
    with columns[0] :
        text = '<h3 align=center>Analyze Data by chatting🔎</h3>'
        # st.write(text,unsafe_allow_html=True)
        st.write(f'<div class="rectangle">{text}</div>', unsafe_allow_html=True)
    with columns[1] :
        text = '<h3 align=center>Train predictive AI models 🤖</h3>'
        st.write(f'<div class="rectangle">{text}</div>', unsafe_allow_html=True)
    with columns[2] :
        text = '<h3 align=center>Deploy them for the further usage 📦</h3'
        st.write(f'<div class="rectangle">{text}</div>', unsafe_allow_html=True)
    with columns[3] :
        text = '<h3 align=center>Without any technical skills 👨‍🔬</h3>'
        st.write(f'<div class="rectangle">{text}</div>', unsafe_allow_html=True)


    columns = st.columns(4)
    with columns[0] :
        text = '<h1 align=center>1.</h1>'
        st.write(text,unsafe_allow_html=True)
        # st.write(f'<div class="rectangle">{text}</div>', unsafe_allow_html=True)
    with columns[1] :
        text = '<h1 align=center>2.</h1>'
        st.write(text,unsafe_allow_html=True)
    with columns[2] :
        text = '<h1 align=center>3.</h1>'
        st.write(text,unsafe_allow_html=True)
    with columns[3] :
        text = '<h1 align=center style="color: green">Done!</h1>'
        st.write(text, unsafe_allow_html=True)



###########################################################################################

def quick_example() :
    # st.markdown('<h1 align=center>Workflow</h1>', unsafe_allow_html=True)
    column1, column2 = st.columns(2)

    with column1 :
        text = '<h3 align=center style="color:cyan">🧑‍💻 What we do<h3>'
        # st.write(f'<div class="rectangle">{text}</div>', unsafe_allow_html=True)
        st.markdown(text, unsafe_allow_html=True)
        code = '''
        # Importing libraries #
        from transformers import pipeline
        from utils import upload_file, preprocess_file
        import chat
        import llm

        # Reading uploaded file #
        df = upload_file()

        # Checking the quality and preprocessing data #
        preprocessed_df = preprocess_file(df)

        # Chatting with the data #
        request = chat.get_user_question()
        answer = llm.post_response(request)

        chat.show_response(answer)
        '''
        st.code(code, language='python')

    with column2 :
        st.markdown('<h3 align=center style="color:pink">💻 What you see<h3>', unsafe_allow_html=True)

        df = pd.DataFrame(data={
            'Country':['France','U.S.A.', 'England', 'Tajikistan'],
            'Capital':['Paris','Washington D.C.', 'London', 'Dushanbe'],
            'Population':[10600, 50000, 45000, 300000],
            'Total area in sq. m.':[234000,456000,43400,25600],
            'Additional info': ['This country is a ...','This country is a ...','This country is a ...','This country is a ...']
        })
        st.write(df)

        with st.chat_message('user') :
            st.write('What is the capital of France?')
        with st.chat_message('assistant') :
            st.write('According to your data, it is Paris')

###########################################################################################