import streamlit as st
import requests
import sqlite3
import pandas as pd

st.set_page_config(page_title='Gestão de Fretes',page_icon='clean.png')
with open("master.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
#
# Side bar menu


menu_option = st.sidebar.radio("Menu", ["Solicitar Embarque", "Requisição x Entradas"])


if menu_option == "Solicitar Embarque":
    
    exec(open("frete_request.py").read())

# Resto do seu código...
if menu_option == "Requisição x Entradas":
    exec(open("visualizador_frete.py").read())
 
        
