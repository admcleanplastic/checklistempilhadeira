import sqlite3
import streamlit as st
import subprocess

# Função para verificar as credenciais de login
def verifica_login(usuario, senha):
    conn = sqlite3.connect('novo.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM usuarios WHERE user = ? AND senha = ?", (usuario, senha))
    resultado = cursor.fetchone()
    conn.close()
    return resultado

# Tela de login
def tela_login():
    st.title("Tela de Login")
    usuario = st.text_input("Usuário")
    senha = st.text_input("Senha", type="password")
    if st.button("Login"):
        resultado = verifica_login(usuario, senha)
        if resultado:
            st.success("Login realizado com sucesso!")
            # Abra o arquivo main.py em um novo navegador
            subprocess.Popen(["streamlit", "run", "main.py"])
            # Encerre o aplicativo atual para evitar conflitos entre os servidores do Streamlit
            raise SystemExit
        else:
            st.error("Credenciais inválidas!")

# Executa a tela de login
tela_login()
