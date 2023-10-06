import streamlit as st
import sqlite3
import pandas as pd
from datetime import datetime
import base64
import xml.etree.ElementTree as ET

st.title('Relatório de entradas')

# Carregar dados do banco de dados SQLite
conn = sqlite3.connect('novo.db')
cursor = conn.cursor()
cursor.execute("SELECT * FROM entrada")
data = cursor.fetchall()
column_names = [description[0] for description in cursor.description]
conn.close()

# Adicione opções para seleção de datas
data_inicial = st.date_input("Data Inicial:")
data_final = st.date_input("Data Final:")

# Filtrar dados com base nas datas selecionadas
filtered_data = []

for row in data:
    try:
        data_formatada = datetime.strptime(row[column_names.index("data")], '%Y-%m-%d').date()
        if data_inicial <= data_formatada <= data_final:
            filtered_data.append(row)
    except ValueError:
        # Ignora entradas com datas incorretas
        pass

# Crie um DataFrame pandas a partir dos dados filtrados
df = pd.DataFrame(filtered_data, columns=column_names)

# Exiba a tabela filtrada
if not df.empty:
    st.write(df)
    
    # Adicione um botão para salvar e baixar em XML
    if st.button('Salvar relatório'):
        # Especifique o caminho completo para salvar o arquivo XML
        xml_file_path = "dados_filtrados.xml"
        
        # Crie um elemento raiz XML
        root = ET.Element("data")
        
        # Adicione os dados do DataFrame como elementos filho
        for index, row in df.iterrows():
            entry = ET.SubElement(root, "entry")
            for col in df.columns:
                ET.SubElement(entry, col).text = str(row[col])
        
        # Crie o arquivo XML
        tree = ET.ElementTree(root)
        tree.write(xml_file_path)
        
        st.success("Relatório salvo com sucesso!")
        
        # Crie um link para download
        with open(xml_file_path, 'rb') as file:
            xml_contents = file.read()
        xml_b64 = base64.b64encode(xml_contents).decode()
        href = f'<a href="data:text/xml;base64,{xml_b64}" download="dados_filtrados.xml">Clique aqui para baixar o relatório</a>'
        st.markdown(href, unsafe_allow_html=True)
else:
    st.warning("Nenhum dado disponível para as datas selecionadas.")
