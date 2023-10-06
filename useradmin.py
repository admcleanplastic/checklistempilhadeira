import streamlit as st
import sqlite3

# Função para criar a tabela de admin se ela não existir
def create_admin_table():
    conn = sqlite3.connect('novo.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS admin (
            ID INTEGER PRIMARY KEY AUTOINCREMENT,
            user TEXT NOT NULL,
            senha TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

# Função para adicionar um administrador à tabela
def add_admin(user, senha):
    conn = sqlite3.connect('novo.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO admin (user, senha) VALUES (?, ?)', (user, senha))
    conn.commit()
    conn.close()

# Função para remover um administrador da tabela
def remove_admin(user_id):
    conn = sqlite3.connect('novo.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM admin WHERE ID = ?', (user_id,))
    conn.commit()
    conn.close()

# Função para listar todos os administradores na tabela
def list_admins():
    conn = sqlite3.connect('novo.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM admin')
    admins = cursor.fetchall()
    conn.close()
    return admins

# Função para editar um administrador na tabela
def edit_admin(user_id, new_user, new_password):
    conn = sqlite3.connect('novo.db')
    cursor = conn.cursor()
    cursor.execute('UPDATE admin SET user = ?, senha = ? WHERE ID = ?', (new_user, new_password, user_id))
    conn.commit()
    conn.close()

# Configuração do Streamlit
st.write('Administradores')

create_admin_table()

# Formulário para adicionar um administrador
st.write('Adicionar Administrador')
new_user = st.text_input('Nome de administrador:')
new_password = st.text_input('Senha:', type='password')
if st.button('Adicionar'):
    if new_user and new_password:
        add_admin(new_user, new_password)
        st.success(f'Administrador "{new_user}" adicionado com sucesso!')

# Lista de administradores existentes
st.write('Administradores Existentes')
admins = list_admins()
if admins:
    st.table(admins)
else:
    st.info('Nenhum administrador cadastrado.')

# Formulário para editar um administrador
st.write('Editar Administrador')
selected_admin = st.selectbox('Selecione um administrador para editar:', admins)
if selected_admin:
    admin_id, old_user, old_password = selected_admin
    new_user = st.text_input('Novo nome de administrador:', old_user)
    new_password = st.text_input('Nova senha:', old_password, type='password')
    if st.button('Editar'):
        edit_admin(admin_id, new_user, new_password)
        st.success(f'Administrador "{old_user}" editado com sucesso!')

# Formulário para remover um administrador
st.write('Remover Administrador')
selected_admin = st.selectbox('Selecione um administrador para remover:', admins)
if selected_admin:
    admin_id = selected_admin[0]
    if st.button('Remover'):
        remove_admin(admin_id)
        st.success(f'Administrador "{selected_admin[1]}" removido com sucesso!')

