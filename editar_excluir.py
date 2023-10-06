

import streamlit as st
import sqlite3
import pandas as pd

# Função para excluir entradas por intervalo de ID
def excluir_por_intervalo_id(id_inicio, id_fim):
    conn = sqlite3.connect('novo.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM entrada WHERE id BETWEEN ? AND ?', (id_inicio, id_fim))
    conn.commit()
    conn.close()

# Função para listar os dados da tabela "entrada" e IDs
def listar_entradas_com_ids(id_inicio, id_fim):
    conn = sqlite3.connect('novo.db')
    query = f'SELECT * FROM entrada WHERE id BETWEEN {id_inicio} AND {id_fim}'
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df

# Configuração do título da página
st.title('Banco de Dados SQLite - Entradas')

# Lista de opções
opcao = st.selectbox('Escolha uma opção:', ['Listar Entradas', 'Excluir por Intervalo de ID'])

if opcao == 'Listar Entradas':
    # Listar entradas
    st.subheader('Lista de Entradas:')
    entradas = listar_entradas_com_ids(1, 1000)  # Defina o intervalo desejado
    st.write(entradas)

elif opcao == 'Excluir por Intervalo de ID':
    # Excluir por intervalo de ID
    st.subheader('Excluir Entradas por Intervalo de ID:')
    id_inicio = st.number_input('Digite o ID de início do intervalo:')
    id_fim = st.number_input('Digite o ID de fim do intervalo:')
    
    if id_inicio > id_fim:
        st.error('O ID de início deve ser menor ou igual ao ID de fim.')
    else:
        if st.button('Excluir'):
            excluir_por_intervalo_id(id_inicio, id_fim)
            st.success(f'Entradas com IDs no intervalo [{id_inicio}, {id_fim}] excluídas com sucesso!')
