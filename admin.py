import datetime 
import csv
import streamlit as st
import sqlite3
import pandas as pd
from datetime import datetime
import base64
st.set_page_config(page_title="Acesso administrador")
# Function to verify login in the database
def login(username, password):
    conn = sqlite3.connect('novo.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM admin WHERE user=? AND senha=?', (username, password))
    user = cursor.fetchone()
    conn.close()
    return user

# Function to update the status in the database
def atualizar_status(selected_id, novo_status):
    conn = sqlite3.connect('novo.db')
    cursor = conn.cursor()
    update_query = "UPDATE entrada SET Status = ? WHERE ID = ?"
    cursor.execute(update_query, (novo_status, selected_id))
    conn.commit()
    conn.close()

# Login page
def login_page():
    st.title('Login Acesso Adiministrador')
    username = st.text_input('Usuário')
    password = st.text_input('Senha', type='password')

    if st.button('Login'):
        user = login(username, password)
        if user is not None:
            st.success('Login realizado com sucesso!')

            # Store login information in the session
            st.session_state.logged_in = True
            st.session_state.user = username

            # Session timeout in seconds (30 minutes)
            session_timeout = 1 * 60

            # Configure session timeout
            st.session_state.session_timeout = session_timeout

        else:
            st.error('Usuário ou senha incorretos.')

# Function to display the menu and functionalities after login
def show_menu():
    menu_option = st.sidebar.radio("Menu Administrador", ["Usuários", "Banco de dados - Entradas", "Usuário Administrador"])

    if menu_option == "Usuários":
        exec(open("server.py").read())
    elif menu_option == "Banco de dados - Entradas":
        exec(open("editar_excluir.py").read())
    elif menu_option == "Usuário Administrador":
        exec(open("useradmin.py").read())
    
    

# Function to log out
def logout():
    st.session_state.logged_in = False
    st.session_state.user = None

# Main application
def main():
    # Check if the user is already logged in
    if not hasattr(st.session_state, 'logged_in') or not st.session_state.logged_in:
        login_page()
        return

    st.write(f'Bem-vindo, {st.session_state.user}!')

    # Logout button in the sidebar
    if st.sidebar.button('Logout'):
        logout()

    # Display the menu and functionalities after login
    show_menu()

if __name__ == '__main__':
    main()
    
import streamlit as st

# Defina seu código CSS dentro de uma string
css = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Roboto:wght@100;300;400&display=swap');
*{
font-family: 'Roboto', sans-serif;


 } 
 table{
 font-size: 10px;
 padding: 250px;
}
   
</style>
"""

# Use st.markdown para incorporar o código CSS
st.markdown(css, unsafe_allow_html=True)

