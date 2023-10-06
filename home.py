import datetime 
import csv
import streamlit as st
import sqlite3
import pandas as pd
from datetime import datetime
import base64




st.set_page_config(page_title="GDE ACESSO_PROD_V1.2")

# Função para verificar login no banco de dados
def login(username, password, selected_table):
    conn = sqlite3.connect('novo.db')
    cursor = conn.cursor()

    if selected_table == "USER_N1":
        cursor.execute('SELECT * FROM usuarios WHERE user=? AND senha=?', (username, password))
    elif selected_table == "USER_ADMIN":
        cursor.execute('SELECT * FROM admin WHERE user=? AND senha=?', (username, password))

    user = cursor.fetchone()
    conn.close()
    return user

# Função para atualizar o status no banco de dados
def atualizar_status(selected_id, novo_status):
    conn = sqlite3.connect('novo.db')
    cursor = conn.cursor()
    update_query = "UPDATE entrada SET Status = ? WHERE ID = ?"
    cursor.execute(update_query, (novo_status, selected_id))
    conn.commit()
    conn.close()

# Página de login
def login_page():
    st.title('Login Acesso')
    username = st.text_input('Usuário')
    password = st.text_input('Senha', type='password')
    
    selected_table = st.selectbox("USER_LEVEL:", ["USER_N1", "USER_ADMIN"])

    if st.button('Login'):
        user = login(username, password, selected_table)
        if user is not None:
            st.success('Login realizado com sucesso!')
            st.write("GDE ACESSO_PROD_V1.2")
            st.write("G.Y.A.M.L")


            # Armazena informações de login na sessão
            st.session_state.logged_in = True
            st.session_state.user = username
            st.session_state.selected_table = selected_table  # Define o nível do usuário na sessão

            # Tempo limite da sessão em segundos (30 minutos)
            session_timeout = 30 * 60

            # Configura o tempo limite da sessão
            st.session_state.session_timeout = session_timeout

        else:
            st.error('Usuário ou senha incorretos.')
#if st.session_state.logged_in:
    #st.write(f"Usuário: {st.session_state.user}")
    

# Função para exibir o menu e funcionalidades após o login
# Função para exibir o menu e funcionalidades após o login
def show_menu():
    # Se o usuário for um administrador, define o menu com opções adicionais
    if st.session_state.selected_table == "USER_ADMIN":
        st.sidebar.markdown('## Menu Administrador')
        menu_option = st.sidebar.radio("Menu", ["Entrada", "Gestão de Entrada", "Inativar Entrada", "Extrair Relatório", "Incluir Operador","Cadastros" "Banco de Dados", "Usuarios Administrador", "Logout"])
    else:
        # Se não for um administrador, define o menu padrão
        st.sidebar.markdown('## Menu')
        menu_option = st.sidebar.radio("Menu", ["Entrada", "Gestão de Entrada", "Inativar Entrada", "Extrair Relatório", "Logout"])
    
    if menu_option == "Entrada":
        exec(open("entrada.py").read())
    elif menu_option == "Inativar Entrada":
        exec(open("inativar_entrada.py").read())
    elif menu_option == "Gestão de Entrada":
        exec(open("gestao_entrada.py").read())    
    elif menu_option == "Extrair Relatório":
        exec(open("relatorio.py").read())
    elif menu_option == "Incluir Operador":
        exec(open("entrada.py").read())
    elif menu_option == "Cadastros":
        exec(open("server.py").read())    
    elif menu_option == "Banco de Dados":
        exec(open("editar_excluir.py").read())
    elif menu_option == "Usuario Administrador":
        exec(open("useradmin.py").read())
    if st.sidebar.button('Logout'):
        logout()  
  
   
       
     
   

# ...

# Função para fazer logout
def logout():
    st.session_state.logged_in = False
    st.session_state.user = None
    st.session_state.selected_table = None  # Remove o nível do usuário da sessão

# Verifica se o usuário está logado antes de exibir o conteúdo
if not hasattr(st.session_state, 'logged_in') or not st.session_state.logged_in:
    login_page()
else:
    show_menu()



custom_css = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@100;300;500;700&family=Roboto:ital,wght@0,300;1,300&display=swap');
   *{

font-family: 'Roboto', sans-serif;
}
</style>
"""

# Use st.markdown para inserir o CSS personalizado
st.markdown(custom_css, unsafe_allow_html=True)

