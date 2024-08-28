import os  # Add this import statement
import streamlit as st
import requests
import time 
from config import backend_url
from utils import get_numerical_concent, stream_data, disable

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

def fetch_unique_drugs_and_districts():
    with st.spinner('🤖 Iniciando Inteligencia Artificial...'):
        unique_drugs = mongo_consult({
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
        })

        for drug in unique_drugs:
            drug['formOption'] = f"{drug['searchTerm']} {drug['concent']} [{drug['nombreFormaFarmaceutica']}]"

        unique_drugs = sorted(unique_drugs, key=lambda x: (
            x['searchTerm'],
            x['nombreFormaFarmaceutica'],
            get_numerical_concent(x['concent'])
        ))

        unique_drugs_names = [doc['formOption'] for doc in unique_drugs]

        unique_distritos = mongo_consult({
            "db": "peru",
            "collection": "districts",
            "aggregation": [
                {"$project": {"_id": 0, "descripcion": 1}},
                {"$sort": {"descripcion": 1}}
            ]
        })
        unique_distritos_names = sorted([doc['descripcion'] for doc in unique_distritos])

        st.session_state.unique_drugs_names = unique_drugs_names
        st.session_state.unique_distritos_names = unique_distritos_names
        st.session_state.unique_drugs = unique_drugs

    intro_message = "¡Hola! Soy tu asistente virtual de búsqueda de medicinas en Lima. Estoy aquí para ayudarte a encontrar las medicinas que necesitas. ¿En qué puedo ayudarte hoy?"
    with st.chat_message("assistant", avatar="🧑‍⚕️"):
        st.write_stream(stream_data(intro_message))
    st.session_state.messages.append({"role": "assistant", "content": intro_message})
    st.session_state.greetings_shown = True

def handle_form_submission():
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

def handle_db_consultation():
    with st.chat_message("assistant", avatar="🧑‍⚕️"):
        st.write_stream(stream_data("Déjame buscar la información que necesitas..."))
        st.session_state.messages.append({"role": "assistant", "content": "Déjame buscar la información que necesitas..."})

    with st.spinner('Buscando medicinas..'):
        find_filtered_drug_body = {
            "db": "health",
            "collection": "drugs",
            "aggregation": [
                {
                    '$match': {
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

    if len(filtered_drugs) > 0:
        with st.chat_message("assistant", avatar="🧑‍⚕️"):
            total_results_message = f"""
            Hay {len(filtered_drugs)} resultados en total \n
            Dejame mostrarte las opciones más económicas:
            """
            st.write_stream(stream_data(total_results_message))
            st.session_state.messages.append({"role": "assistant", "content": total_results_message})

        st.session_state.search_results = filtered_drugs
        st.session_state['top3'] = filtered_drugs

        for drug in filtered_drugs:
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
        st.page_link(os.environ.get("DOMAIN"), label="Realizar otra consulta", icon="💊")