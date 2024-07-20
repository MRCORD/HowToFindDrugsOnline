import streamlit as st
import requests
import pandas as pd

import re
import time

# --- Envs ---

from dotenv import load_dotenv
import os

# --- Analytics ---

from posthog import Posthog
import uuid


load_dotenv()

st.set_page_config(
    page_title="Busca tu Pepa",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.title("Busca tu Pepa 💊")

backend_url = os.environ.get("BACKEND_URL")
domain = os.environ.get("DOMAIN")
posthog_key = os.environ.get("POSTHOG_API_KEY")


posthog = Posthog(project_api_key=posthog_key, host='https://us.i.posthog.com')

posthog.capture('distinct_id_of_the_user', '$pageview', {'$current_url': domain})


#@st.cache_data(ttl=600)
def mongo_consult(consult_body):
    try:
        response = requests.post(f"{backend_url}/v1/consult_mongo", json=consult_body)
        
        if response.status_code == 200:
            response_json = response.json()
            return response_json.get('documents', [])
        else:
            return []
    except Exception as e:
        st.error(f"An error occurred: {e}")
        return []
    

# Define the consultation bodies for MongoDB
consult_unique_drugs = {
    "db": "health",
    "collection": "drugs",
    "aggregation": [
        {"$group": {
                "_id": {
                    "searchTerm": "$searchTerm",
                    "concent": "$producto.concent",
                    "nombreFormaFarmaceutica": "$producto.nombreFormaFarmaceutica"
                }}},
        {"$sort": {
                "_id.searchTerm": 1,
                "_id.concent": 1,
                "_id.nombreFormaFarmaceutica": 1
            }},
        {"$project": {
                "_id": 0,
                "searchTerm": "$_id.searchTerm",
                "concent": "$_id.concent",
                "nombreFormaFarmaceutica": "$_id.nombreFormaFarmaceutica"
            }}
    ]
}

consult_unique_distritos = {
    "db": "peru",
    "collection": "districts",
    "aggregation": [
        {"$project": {"_id": 0, "descripcion": 1}},
        {"$sort": {"descripcion": 1}}
    ]
}


# Function to extract the numerical part of the concentration using regular expressions
def get_numerical_concent(concent):
    numbers = re.findall(r'\d+\.?\d*', concent)  # Find all numbers (integers or decimals)
    return float(numbers[0]) if numbers else 0  # Convert the first found number to float, default to 0 if none found



def display_chat_messages() -> None:
    """Print message history
    @returns None
    """
    for message in st.session_state.messages:
        with st.chat_message(message["role"],avatar="🧑‍⚕️"):
            st.markdown(message["content"])

def stream_data(string):
    for word in string.split(" "):
        yield word + " "
        time.sleep(0.06)
        
        
# Disable the submit button after it is clicked
def disable():
    st.session_state.disabled = True

# Initialize disabled for form_submit_button to False
if "disabled" not in st.session_state:
    st.session_state.disabled = False
    
col1, col2, col3 = st.columns([0.2, 0.5, 0.2])


# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

if 'concentrations_shown' not in st.session_state:
    st.session_state['concentrations_shown'] = False 
    st.session_state['clicked_concentration'] = None

# Display chat messages from history on app rerun
display_chat_messages()

# Initialize session state variables if they don't exist
if 'greetings_shown' not in st.session_state:
    st.session_state['greetings_shown'] = False
    
if 'form_submitted' not in st.session_state:
    st.session_state['form_submitted'] = False


if not st.session_state.greetings_shown:
    
    with st.spinner('🤖 Iniciando Inteligencia Artificial...'):
        # time.sleep(5)

        # Fetch unique drug and district names
        unique_drugs = mongo_consult(consult_unique_drugs)

        # Assuming unique_drugs is a list of dictionaries as described
        for drug in unique_drugs:
            # Concatenate the required strings and add them under the new key 'formOption'
            drug['formOption'] = f"{drug['searchTerm']} {drug['concent']} [{drug['nombreFormaFarmaceutica']}]"



        # Sorting the list with a custom key that handles numerical sorting for `concent`
        unique_drugs = sorted(unique_drugs, key=lambda x: (
            x['searchTerm'],
            x['nombreFormaFarmaceutica'],
            get_numerical_concent(x['concent'])
        ))

        unique_drugs_names = [doc['formOption'] for doc in unique_drugs]

        unique_distritos = mongo_consult(consult_unique_distritos)
        unique_distritos_names = sorted([doc['descripcion'] for doc in unique_distritos])
        
        st.session_state.unique_drugs_names = unique_drugs_names
        st.session_state.unique_distritos_names = unique_distritos_names
        st.session_state.unique_drugs = unique_drugs
        
    
    intro_message = "¡Hola! Soy tu asistente virtual de búsqueda de medicinas en Lima. Estoy aquí para ayudarte a encontrar las medicinas que necesitas. ¿En qué puedo ayudarte hoy?"
    
    with st.chat_message("assistant", avatar="🧑‍⚕️"):
        st.write_stream(stream_data(intro_message))
        
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": intro_message})
    st.session_state.greetings_shown = True
    
if not st.session_state.form_submitted:
    
    consult_form = st.empty()
    
    with consult_form.form(key='consult_form'):
        selector_drugs = st.selectbox('Medicina', st.session_state.unique_drugs_names, index=None, placeholder="Selecciona la medicina...")
        selector_distritos = st.selectbox('Distrito', st.session_state.unique_distritos_names, index=None, placeholder="Selecciona el distrito...")
        submit = st.form_submit_button('Consultar', on_click=disable, disabled=st.session_state.disabled)
        
    if submit:
        matching_item = [drug for drug in st.session_state.unique_drugs if drug['formOption'] == selector_drugs]
        
        requested_search = {
            "selected_drug": matching_item[0]['searchTerm'],
            "concent": matching_item[0]['concent'],
            "nombreFormaFarmaceutica": matching_item[0]['nombreFormaFarmaceutica'],
            "selected_distrito": selector_distritos
        }
        
        st.session_state.requested_search = requested_search
        
        consult_form = st.empty()
        
        # with st.chat_message("user"):
        #     form_request = f"Quiero buscar información sobre {requested_search['selected_drug']} en el distrito {requested_search['selected_distrito']}"
        #     st.write_stream(stream_data(form_request))
        
        # st.session_state.form_submitted = True
        # st.session_state.messages.append({"role": "user", "content": form_request})
        
        
        

if 'db_consulted' not in st.session_state:
    st.session_state['db_consulted'] = False
    
if 'concentrations_loaded' not in st.session_state:
    st.session_state['concentrations_loaded'] = False  
    

if not st.session_state.db_consulted and 'requested_search' in st.session_state:
    
    with st.chat_message("assistant", avatar="🧑‍⚕️"):
        st.write_stream(stream_data("Déjame buscar la información que necesitas..."))
        st.session_state.messages.append({"role": "assistant", "content": "Déjame buscar la información que necesitas..."})
        
    with st.spinner('Buscando medicinas..'):

        #Query MongoDb
        find_filtered_drug_body = {
            "db": "health",
            "collection": "drugs",
            # "query": 
            #     "searchTerm": st.session_state.requested_search['selected_drug'],
            #     "producto.concent": st.session_state.requested_search['concent'],
            #     "producto.nombreFormaFarmaceutica": st.session_state.requested_search['nombreFormaFarmaceutica'],
            #     "comercio.locacion.distrito": st.session_state.requested_search['selected_distrito']
            # 
            "aggregation": [
            {
                '$match': {
                    # 'searchTerm': 'AMITRIPTILINA CLORHIDRATO', 
                    # 'producto.concent': '25 mg', 
                    # 'producto.nombreFormaFarmaceutica': 'Tableta Recubierta', 
                    # 'comercio.locacion.distrito': 'MIRAFLORES'
                    "searchTerm": st.session_state.requested_search['selected_drug'],
                    "producto.concent": st.session_state.requested_search['concent'],
                    "producto.nombreFormaFarmaceutica": st.session_state.requested_search['nombreFormaFarmaceutica'],
                    "comercio.locacion.distrito": st.session_state.requested_search['selected_distrito']
                }
            }, {
                '$sort': {
                    'producto.precios.precio2': 1
                }
            }, {
                '$limit': 3
            }, {
                '$lookup': {
                    'from': 'pharmacies', 
                    'localField': 'comercio.pharmacyId', 
                    'foreignField': '_id', 
                    'as': 'pharmacyInfo'
                }
            }, {
                '$project': {
                    '_id': 1, 
                    'nombreProducto': '$producto.nombreProducto', 
                    'concent': '$producto.concent', 
                    'nombreFormaFarmaceutica': '$producto.nombreFormaFarmaceutica', 
                    'precio2': '$producto.precios.precio2', 
                    'nombreComercial': {
                        '$arrayElemAt': [
                            '$pharmacyInfo.nombreComercial', 0
                        ]
                    }, 
                    'direccion': {
                        '$arrayElemAt': [
                            '$pharmacyInfo.locacion.direccion', 0
                        ]
                    }, 
                    'googleMaps_search_url': {
                        '$arrayElemAt': [
                            '$pharmacyInfo.google_maps.googleMaps_search_url', 0
                        ]
                    }, 
                    'googleMapsUri': {
                        '$arrayElemAt': [
                            '$pharmacyInfo.google_maps.googleMapsUri', 0
                        ]
                    }
                }
            }
        ]
        }   

        filtered_drugs = mongo_consult(find_filtered_drug_body)
        
        # time.sleep(2)
    
    if len(filtered_drugs) > 0:
        
        #Retrieve drugs
        with st.chat_message("assistant", avatar="🧑‍⚕️"):
            total_results_message = f"""
            Hay {len(filtered_drugs)} resultados en total \n
            Dejame mostrarte las opciones más económicas:
            """
            st.write_stream(stream_data(total_results_message))
            st.session_state.messages.append({"role": "assistant", "content": total_results_message})
            

        #Store retrieved drugs
        st.session_state.search_results = filtered_drugs
        
        # sorted_filtered_drugs = sorted(
        # filtered_drugs,
        # key=lambda d: float(d.get('producto', {}).get('precios', {}).get('precio2', float('inf'))),
        # # Using float('inf') as a default value to handle missing keys or values
        # )
        
        # top_3_filtered_drugs = sorted_filtered_drugs[:3]
        
        st.session_state['top3'] = filtered_drugs #top_3_filtered_drugs
        
            
        for drug in filtered_drugs: #top_3_filtered_drugs:
            # drug_name = drug['producto']['nombreProducto']
            # drug_concent = drug['producto']['concent']
            # drug_forma = drug['producto']['nombreFormaFarmaceutica']
            # drug_price = drug['producto']['precios']['precio2']
            
            # drug_comercio = drug['comercio']['nombreComercial']
            # drug_ubicacion = drug['comercio']['locacion']['direccion']
            
            drug_name = drug.get('nombreProducto')
            drug_concent = drug.get('concent')
            drug_forma = drug.get('nombreFormaFarmaceutica')
            drug_price = drug.get('precio2')
            
            drug_comercio = drug.get('nombreComercial')
            drug_ubicacion = drug.get('direccion')
            google_maps_url_search = drug.get('googleMaps_search_url')
            google_maps_url = drug.get('googleMapsUri')
            
            with st.chat_message("assistant", avatar="🧑‍⚕️"):
                
                if google_maps_url:
                    url_mkdown = f"[{drug_comercio}: {drug_ubicacion}]({google_maps_url})"
                else:
                    url_mkdown = f"[{drug_comercio}: {drug_ubicacion}]({google_maps_url_search})"

                drug_message = f"""
                🔍 {drug_name} {drug_concent} [{drug_forma}] - Precio: S/. {drug_price} \n
                📍 {url_mkdown} \n
                """

                st.write_stream(stream_data(drug_message))
                #st.markdown(f"{url_mkdown}")
                st.session_state.messages.append({"role": "assistant", "content": drug_message})
        
        st.session_state.db_consulted = True
    
    else:
        with st.chat_message("assistant", avatar="🧑‍⚕️"):
            total_results_message = f"""
            No se encontraron resultados para {st.session_state.requested_search['selected_drug']} en el distrito {st.session_state.requested_search['selected_distrito']}
            """
            st.write_stream(stream_data(total_results_message))
            st.session_state.messages.append({"role": "assistant", "content": total_results_message})
    
    time.sleep(2)
    
    with st.chat_message("assistant", avatar="🧑‍⚕️"):
        restart_message = f"""Deseas realizar otra consulta? Presiona el botón de abajo para realizar otra consulta ⬇️"""
        
        st.write_stream(stream_data(restart_message))
        
        st.page_link( domain , label="Realizar otra consulta", icon="💊")