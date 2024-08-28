import streamlit as st
from dotenv import load_dotenv
import os
from analytics import initialize_posthog, capture_pageview, load_gtm  # Import the load_gtm function
from utils import display_chat_messages, stream_data, disable
from consultations import fetch_unique_drugs_and_districts, handle_form_submission, handle_db_consultation

# Streamlit Config
st.set_page_config(
    page_title="Busca tu Pepa",
    page_icon="🏥",
    # layout="wide",
    initial_sidebar_state="expanded",
)


# Load environment variables
load_dotenv()

# Load Google Tag Manager
load_gtm('G-SY9SGNP6C2')  # Replace 'GTM-XXXXXXX' with your GTM ID


st.title("Busca tu Pepa 💊")

# Initialize Analytics
posthog = initialize_posthog()
capture_pageview(posthog)

# Session State Initialization
if "disabled" not in st.session_state:
    st.session_state.disabled = False

if "messages" not in st.session_state:
    st.session_state.messages = []

if 'concentrations_shown' not in st.session_state:
    st.session_state.concentrations_shown = []

if 'greetings_shown' not in st.session_state:
    st.session_state['greetings_shown'] = False

if 'form_submitted' not in st.session_state:
    st.session_state['form_submitted'] = False

if 'db_consulted' not in st.session_state:
    st.session_state['db_consulted'] = False

if 'concentrations_loaded' not in st.session_state:
    st.session_state['concentrations_loaded'] = False

# Main Logic
display_chat_messages()

if not st.session_state.greetings_shown:
    fetch_unique_drugs_and_districts()

if not st.session_state.form_submitted:
    handle_form_submission()

if not st.session_state.db_consulted and 'requested_search' in st.session_state:
    handle_db_consultation()