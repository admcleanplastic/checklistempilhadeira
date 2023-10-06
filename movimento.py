import streamlit as st
import sqlite3
import pandas as pd

# Conectar ao banco de dados
conn = sqlite3.connect('novo.db')

# Carregar os dados em um DataFrame
df = pd.read_sql_query('SELECT * FROM entrada_saida', conn)

# Filtro de data
filtro_data = st.date_input("Filtrar por data")

# Filtro de motivo
filtro_motivo = st.selectbox("Filtrar por motivo", df['motivo'].unique())

# Aplicar filtros
if filtro_data:
    filtro_data = pd.to_datetime(filtro_data)
    df['data'] = pd.to_datetime(df['data'])
    df = df[df['data'].dt.date == filtro_data.date()]

if filtro_motivo:
    df = df[df['motivo'] == filtro_motivo]

# Verificar se há dados após os filtros
if df.empty:
    st.write('Nenhum dado encontrado.')
else:
    # Exibir o DataFrame filtrado como uma tabela
    for index, row in df.iterrows():
        if st.button('Chamar', key=f'button_{index}'):
            # Alterar a cor da linha quando o botão é acionado
            st.markdown(
                f'<style>.row-index-{index} .stButton button {{background-color: yellow}}</style>',
                unsafe_allow_html=True
            )
        
        # Exibir os dados da linha atual
        st.write(row)

# Fechar a conexão com o banco de dados
conn.close()
