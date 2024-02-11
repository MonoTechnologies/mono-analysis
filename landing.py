import streamlit as st
from streamlit import session_state as state

def main_page() :
    # Showing the title #
    st.title("💬 Mono-Chat")

    # Showing Additional information #
    with st.expander('Want to learn more?') :
        st.write('Mono-Chat powered by Mono-Analysis')
        st.write('v1.0.0')
