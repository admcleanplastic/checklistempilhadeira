import streamlit as st
import sqlite3

# Função para criar a tabela de usuários se ela não existir
def create_user_table():
    conn = sqlite3.connect('novo.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS operador (
            ID INTEGER PRIMARY KEY AUTOINCREMENT,
            user TEXT NOT NULL,
            senha TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

# Função para adicionar um usuário à tabela
def add_user(user, senha):
    conn = sqlite3.connect('novo.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO operador (user, senha) VALUES (?, ?)', (user, senha))
    conn.commit()
    conn.close()

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

# Função para editar um usuário na tabela
def edit_user(user_id, new_user, new_password):
    conn = sqlite3.connect('novo.db')
    cursor = conn.cursor()
    cursor.execute('UPDATE operador SET user = ?, senha = ? WHERE ID = ?', (new_user, new_password, user_id))
    conn.commit()
    conn.close()

# Configuração do Streamlit
st.write('Usuários')

create_user_table()

# Formulário para adicionar um usuário
st.write('Adicionar Usuário')
new_user = st.text_input('Nome de usuário:')
new_password = st.text_input('Senha:', type='password')
if st.button('Adicionar'):
    if new_user and new_password:
        add_user(new_user, new_password)
        st.success(f'Usuário "{new_user}" adicionado com sucesso!')

# Lista de usuários existentes
st.write('Usuários Existentes')
users = list_users()
if users:
    st.table(users)
else:
    st.info('Nenhum usuário cadastrado.')

# Formulário para editar um usuário
st.write('Editar Usuário')
selected_user = st.selectbox('Selecione um usuário para editar:', users)
if selected_user:
    user_id, old_user, old_password = selected_user
    new_user = st.text_input('Novo nome de usuário:', old_user)
    new_password = st.text_input('Nova senha:', old_password, type='password')
    if st.button('Editar'):
        edit_user(user_id, new_user, new_password)
        st.success(f'Usuário "{old_user}" editado com sucesso!')

# Formulário para remover um usuário
st.write('Remover Usuário')
selected_user = st.selectbox('Selecione um usuário para remover:', users)
if selected_user:
    user_id = selected_user[0]
    if st.button('Remover'):
        remove_user(user_id)
        st.success(f'Usuário "{selected_user[1]}" removido com sucesso!')
