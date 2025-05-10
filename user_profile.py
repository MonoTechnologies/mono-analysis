import streamlit as st
from streamlit import session_state as state

from utils import *

def start() -> None :
    st.markdown("<h1 style='text-align: center;'>My Profile</h1>", unsafe_allow_html=True)
    hr()

    # Getting user's data #
    user_info = get_docs('users_db')
    user_info = user_info[ user_info['username'] == state['username'] ]
    user_info = pd.Series( user_info.iloc[0] )

    # st.write(user_info)

    # Displaying Username #
    st.header( f"Username: :blue[{user_info['username']}]" )

    # Displaying Account type #
    acc_text_color = 'rainbow' if user_info['type'] == 'admin' else 'green'
    st.header( f"Account type: :{acc_text_color}[{user_info['type']}]" )

    # Displaying registry date #
    timestamp = user_info['registered_at']
    year = timestamp.year
    month = timestamp.month
    day = timestamp.day
    hour = timestamp.hour
    minute = timestamp.minute

    if hour < 10 :
        hour = '0'+str((hour))

    if minute < 10 :
        minute = '0'+str((minute))

    st.header( f"Registry date: {year}-{month}-{day} at {hour}:{minute}" )