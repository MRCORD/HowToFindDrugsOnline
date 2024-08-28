import streamlit as st
import re
import time

def display_chat_messages():
    for message in st.session_state.messages:
        with st.chat_message(message["role"], avatar="🧑‍⚕️"):
            st.markdown(message["content"])

def stream_data(string):
    for word in string.split(" "):
        yield word + " "
        time.sleep(0.06)

def disable():
    st.session_state.disabled = True

def get_numerical_concent(concent):
    numbers = re.findall(r'\d+\.?\d*', concent)
    return float(numbers[0]) if numbers else 0