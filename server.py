import sqlite3
import streamlit as st
from datetime import date

# Função para remover um usuário da tabela
def remove_user(user_id):
    conn = sqlite3.connect('novo.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM operador WHERE ID = ?', (user_id,))
    conn.commit()
    conn.close()

# Função para listar todos os usuários na tabela
def list_users():
    conn = sqlite3.connect('novo.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM operador')
    users = cursor.fetchall()
    conn.close()
    return users

# Função para adicionar um usuário à tabela
def add_user(data, empresa, nome_completo, usuario, turno, setor, senha, equipamento):
    conn = sqlite3.connect('novo.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO operador (data, empresa, nome_completo, user, turno, setor, senha, equipamento) VALUES (?, ?, ?, ?, ?, ?, ?, ?)',
                   (data, empresa, nome_completo, usuario, turno, setor, senha, equipamento))
    conn.commit()
    conn.close()

# Função para editar um usuário na tabela
def edit_user(user_id, data, empresa, nome_completo, usuario, turno, setor, senha, equipamento):
    conn = sqlite3.connect('novo.db')
    cursor = conn.cursor()
    cursor.execute('UPDATE operador SET data = ?, empresa = ?, nome_completo = ?, user = ?, turno = ?, setor = ?, senha = ?, equipamento = ? WHERE ID = ?',
                   (data, empresa, nome_completo, usuario, turno, setor, senha, equipamento, user_id))
    conn.commit()
    conn.close()

# Configuração do Streamlit
st.write('Usuários')

# Formulário para editar um usuário
st.write('Editar Usuário')
users = list_users()
selected_user = st.selectbox('Selecione um usuário para editar:', users)
if selected_user:
    user_id, data, empresa, nome_completo, usuario, turno, setor, senha, equipamento = selected_user
    new_data = st.date_input("Data", value=date.today(), key="data")
    new_empresa = st.selectbox('Empresa', ['Clean Plastic'], index=0 if empresa == 'Clean Plastic' else 1)
    new_nome_completo = st.text_input("Nome Completo:", value=nome_completo).upper()
    new_usuario = st.text_input("Usuário", value=usuario).upper()
    new_turno = st.selectbox('Turno:', ['1º Turno', '2º Turno', '3º Turno', 'ADM'], index=['1º Turno', '2º Turno', '3º Turno', 'ADM'].index(turno))
    new_setor = st.selectbox('Setor:', ['Blenda', 'Recebimento', 'Logística'], index=['Blenda', 'Recebimento', 'Logística'].index(setor))
    new_senha = st.text_input('Senha', value=senha, type='password')
    new_equipamento = st.selectbox('Equipamento:', ['Empilhadeira Recebimento 01'], index=0)

    if st.button('Editar'):
        edit_user(user_id, new_data, new_empresa, new_nome_completo, new_usuario, new_turno, new_setor, new_senha, new_equipamento)
        st.success(f'Usuário "{nome_completo}" editado com sucesso!')

# Formulário para remover um usuário
st.write('Remover Usuário')
if users:
    selected_user = st.selectbox('Selecione um usuário para remover:', users)
    if selected_user:
        user_id = selected_user[0]
        if st.button('Remover'):
            remove_user(user_id)
            st.success(f'Usuário "{selected_user[3]}" removido com sucesso!')

# Lista de usuários existentes
st.write('Usuários Existentes')
if users:
    st.table(users)
else:
    st.info('Nenhum usuário cadastrado.')
