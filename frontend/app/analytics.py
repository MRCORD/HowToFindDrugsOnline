from posthog import Posthog
from config import posthog_key, domain
import streamlit as st

def initialize_posthog():
    return Posthog(project_api_key=posthog_key, host='https://us.i.posthog.com')

def capture_pageview(posthog):
    posthog.capture('distinct_id_of_the_user', '$pageview', {'$current_url': domain})

def load_gtm(gtm_id):
    gtm_script = f"""
    <!-- Google Tag Manager -->
    <script>(function(w,d,s,l,i){{w[l]=w[l]||[];w[l].push({{'gtm.start':
    new Date().getTime(),event:'gtm.js'}});var f=d.getElementsByTagName(s)[0],
    j=d.createElement(s),dl=l!='dataLayer'?'&l='+l:'';j.async=true;j.src=
    'https://www.googletagmanager.com/gtm.js?id='+i+dl;f.parentNode.insertBefore(j,f);
    }})(window,document,'script','dataLayer','{gtm_id}');</script>
    <!-- End Google Tag Manager -->
    """
    st.components.v1.html(gtm_script, height=0, width=0)