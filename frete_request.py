import sqlite3
import csv
import streamlit as st
from datetime import date

st.title('Solicitar Embarque')

# Função para obter os municípios de um estado específico
def obter_municipios(estado):
    municipios = []

    # Caminho para o arquivo CSV local
    arquivo_csv = 'dados.csv'

    with open(arquivo_csv, 'r', newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file, delimiter=';')
        for row in reader:
            if 'UF' in row and row['UF'] == estado:
                municipios.append(row['Município'])

    return municipios

# Obtém a lista de estados
estados = []
arquivo_csv = 'dados.csv'

with open(arquivo_csv, 'r', newline='', encoding='utf-8') as file:
    reader = csv.DictReader(file, delimiter=';')
    for row in reader:
        if 'UF' in row:
            estado = row['UF']
            if estado not in estados:
                estados.append(estado)

today = date.today()
data_solicitacao = st.date_input("Data da solicitação", value=today, disabled=True)
empresa_origem = st.selectbox('Empresa Origem/local de Coleta', ['Clean Plastic', 'Clean Poa', 'Clean Jundiai', 'Clean Bottle', 'Clean Fortal', 'Raposo Plasticos', 'Raposo Minas', 'Fornecedor PF', 'Outro'])

col1, col2 = st.columns(2)
today = date.today()

with col1:
    estado_origem = st.selectbox('Selecione o estado de origem', estados)
    municipios_origem = obter_municipios(estado_origem)
    cidade_origem = st.selectbox('Selecione a cidade de origem', municipios_origem)
    estado_destino = st.selectbox('Selecione o estado de destino', estados)
    municipios_destino = obter_municipios(estado_destino)
    cidade_destino = st.selectbox('Selecione a cidade de destino', municipios_destino)

with col2:
    data_coleta = st.date_input("Data da coleta", value=today, key="data_input")
    data_entrega = st.date_input("Data da Entrega", value=today, key="")
    tipo_veiculo = st.selectbox("Tipo de Veiculo", ["Truck-Side", "Carreta-Side", "Truck-Grade Baixa", "Carreta-Grade Baixa", "Carreta Graneleira", "Container"])
observacao = st.text_area("Observacoes")

# Save button
if st.button("Salvar"):
    # Connect to the database or create a new one if it doesn't exist
    conn = sqlite3.connect('novo.db')

    # Create a cursor object to execute SQL queries
    cursor = conn.cursor()

    # Create the 'frete' table if it doesn't exist
    cursor.execute('''CREATE TABLE IF NOT EXISTS frete (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        data_solicitacao TEXT,
                        empresa_origem TEXT,
                        estado_origem TEXT,
                        cidade_origem TEXT,
                        estado_destino TEXT,
                        cidade_destino TEXT,
                        tipo_veiculo TEXT,
                        data_coleta TEXT,
                        data_entrega TEXT,
                        observacao TEXT
                    )''')

    # Get the values from the fields
    data_solicitacao_value = date.today().strftime("%Y-%m-%d")
    empresa_origem_value = empresa_origem
    estado_origem_value = estado_origem
    cidade_origem_value = cidade_origem
    estado_destino_value = estado_destino
    cidade_destino_value = cidade_destino
    tipo_veiculo_value = tipo_veiculo
    data_coleta_value = data_coleta.strftime("%Y-%m-%d")
    data_entrega_value = data_entrega.strftime("%Y-%m-%d")
    observacao_value = observacao

    # Insert the values into the 'frete' table
    cursor.execute('''INSERT INTO frete (
                        data_solicitacao,
                        empresa_origem,
                        estado_origem,
                        cidade_origem,
                        estado_destino,
                        cidade_destino,
                        tipo_veiculo,
                        data_coleta,
                        data_entrega,
                        observacao
                    )
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                    (data_solicitacao_value, empresa_origem_value, estado_origem_value, cidade_origem_value, estado_destino_value, cidade_destino_value, tipo_veiculo_value, data_coleta_value, data_entrega_value, observacao_value))

    # Commit the changes and close the connection
    conn.commit()
    conn.close()
    st.success("Dados salvos com sucesso!")
