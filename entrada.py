import sqlite3
import streamlit as st
from datetime import date

st.title("Inclusão de Operador")

# Data de entrada não pode ser alterada!
data = st.date_input("Data", value=date.today(), key="data")

Empresa = st.selectbox('Empresa', ['Clean Plastic'])

col1, col2 = st.columns(2)
with col1:
    Nome_completo = st.text_input("Nome Completo:").upper()
    user = st.text_input("Usuário").upper()
    Turno = st.selectbox('Turno:', ['1º Turno', '2º Turno', '3º Turno', 'ADM'])

with col2:
    Setor = st.selectbox('Setor:', ['Blenda', 'Recebimento', 'Logística'])
    senha = st.text_input('Senha', type='password')
    Equipamento = st.selectbox('Equipamento:', ['Empilhadeira Recevimento 01'])

def is_form_valid(data, Nome_completo, user, Turno, Setor, password, Equipamento):
    required_fields = [
        data,
        Nome_completo,
        user,
        Turno,
        Setor,
        password,
        Equipamento,
    ]

    for field in required_fields:
        if not field:
            return False

    return True

if st.button("Salvar"):
    if is_form_valid(data, Nome_completo, user, Turno, Setor, password, Equipamento):
        # Conectar ao banco de dados ou criar um novo se ele não existir
        conn = sqlite3.connect('novo.db')

        # Criar um objeto cursor para executar consultas SQL
        cursor = conn.cursor()

        # Criar a tabela 'operador' se ela não existir
        cursor.execute('''CREATE TABLE IF NOT EXISTS operador (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        data TEXT,
                        Nome_completo TEXT,
                        user TEXT,
                        Turno TEXT,
                        Setor TEXT,
                        password TEXT,
                        Equipamento TEXT
                    )''')

        # Obter os valores dos campos
        data_value = data.strftime("%Y-%m-%d")
        Nome_completo_value = Nome_completo
        user_value = user
        Turno_value = Turno
        Setor_value = Setor
        password_value = password
        Equipamento_value = Equipamento

        # Inserir os valores na tabela 'operador'
        cursor.execute('''INSERT INTO operador (
                        data,
                        Nome_completo,
                        user,
                        Turno,
                        Setor,
                        password,
                        Equipamento
                    )
                    VALUES (?, ?, ?, ?, ?, ?, ?)''',
                   (
                       data_value,
                       Nome_completo_value,
                       user_value,
                       Turno_value,
                       Setor_value,
                       password_value,
                       Equipamento_value
                   ))

        # Confirmar as alterações e fechar a conexão
        conn.commit()
        conn.close()
        st.success("Dados salvos com sucesso!")
    else:
        st.warning("Preencha todos os campos antes de salvar.")

