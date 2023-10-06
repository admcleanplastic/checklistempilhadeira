import sqlite3
import streamlit as st

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
def edit_user(user_id, new_user, new_password, new_nome, new_email):
    conn = sqlite3.connect('novo.db')
    cursor = conn.cursor()
    cursor.execute('UPDATE operador SET user = ?, senha = ?, nome = ?, email = ? WHERE ID = ?', (new_user, new_password, new_nome, new_email, user_id))
    conn.commit()
    conn.close()

# Configuração do Streamlit
st.write('Usuários')

# Formulário para editar um usuário
st.write('Editar Usuário')
users = list_users()
selected_user = st.selectbox('Selecione um usuário para editar:', users)
if selected_user:
    user_id, old_user, old_password, old_nome, old_email = selected_user
    new_user = st.text_input('Novo nome de usuário:', old_user)
    new_password = st.text_input('Nova senha:', old_password, type='password')
    new_nome = st.text_input('Novo nome:', old_nome)
    new_email = st.text_input('Novo email:', old_email)
    if st.button('Editar'):
        edit_user(user_id, new_user, new_password, new_nome, new_email)
        st.success(f'Usuário "{old_user}" editado com sucesso!')

# Formulário para remover um usuário
st.write('Remover Usuário')
selected_user = st.selectbox('Selecione um usuário para remover:', users)
if selected_user:
    user_id = selected_user[0]
    if st.button('Remover'):
        remove_user(user_id)
        st.success(f'Usuário "{selected_user[1]}" removido com sucesso!')

# Lista de usuários existentes
st.write('Usuários Existentes')
if users:
    st.table(users)
else:
    st.info('Nenhum usuário cadastrado.')
