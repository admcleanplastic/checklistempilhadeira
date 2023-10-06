import streamlit as st
import sqlite3
from datetime import date, timedelta

# Função para atualizar o status no banco de dados
def atualizar_status(id, novo_status):
    conn = sqlite3.connect('novo.db')
    cursor = conn.cursor()
    cursor.execute("UPDATE entrada SET Status = ? WHERE ID = ?", (novo_status, id))
    conn.commit()
    conn.close()

# Função para carregar dados com base nos filtros e substituir valores nulos por "Aguardando Entrada"
def carregar_dados(start_date, end_date, selected_motivo, selected_local, selected_status):
    conn = sqlite3.connect('novo.db')
    cursor = conn.cursor()
    
    # Construir a consulta SQL com base nos filtros e substituir valores nulos por "Aguardando Entrada"
    query = "SELECT * FROM entrada WHERE 1 = 1"
    params = []
    
    if start_date:
        query += " AND DATE(data) >= ?"
        params.append(start_date)
    
    if end_date:
        query += " AND DATE(data) <= ?"
        params.append(end_date)
    
    if selected_motivo:
        query += " AND motivo = ?"
        params.append(selected_motivo)
    
    if selected_local:
        query += " AND local_entrada = ?"
        params.append(selected_local)
    
    if selected_status:
        query += " AND (Status = ? OR Status IS NULL)"  # Considerar valores nulos como "Aguardando Entrada"
        params.append(selected_status)
    else:
        query += " AND (Status IS NULL OR Status = 'Aguardando Entrada')"  # Se nenhum status selecionado, incluir "Aguardando Entrada"
    
    # Adicionar condição para ocultar registros com Status "Inativo"
    query += " AND (Status IS NULL OR Status != 'Inativo')"
    
    cursor.execute(query, params)
    data = cursor.fetchall()
    conn.close()
    return data

# Mapear cores para Status
status_colors = {
    "Aguardando Entrada": "",
    "Liberar Entrada": "yellow",
    "Descarregando": "lightblue",
    "Carregando": "orange",
    "Finalizado": "green",
    "Inativo": ""
}

# Configuração da página Streamlit
st.title("Atualização de status de entrada")

# Conexão com o banco de dados SQLite
conn = sqlite3.connect('novo.db')
cursor = conn.cursor()

# Consulta para obter os nomes das colunas da tabela "entrada"
cursor.execute("PRAGMA table_info(entrada)")
column_info = cursor.fetchall()
column_names = [info[1] for info in column_info]

# Consulta para obter todos os valores únicos das colunas "motivo", "local_entrada" e "Status"
cursor.execute("SELECT DISTINCT motivo FROM entrada")
motivos = [row[0] for row in cursor.fetchall()]

cursor.execute("SELECT DISTINCT local_entrada FROM entrada")
locais = [row[0] for row in cursor.fetchall()]

cursor.execute("SELECT DISTINCT Status FROM entrada")
status = [row[0] for row in cursor.fetchall()]

# Fechar a conexão com o banco de dados
conn.close()

# Sidebar para filtros de data, motivo, local_entrada e Status
st.sidebar.title("Filtros")
start_date = st.sidebar.date_input("Selecione a data de início:", date.today())
end_date = st.sidebar.date_input("Selecione a data de término:", date.today())
selected_motivo = st.sidebar.selectbox("Selecione o motivo:", [""] + motivos)
selected_local = st.sidebar.selectbox("Selecione o local de entrada:", [""] + locais)
selected_status = st.sidebar.selectbox("Selecione o Status:", [""] + status)

# Carregar dados com base nos filtros
filtered_data = carregar_dados(start_date, end_date, selected_motivo, selected_local, selected_status)

# Filtrar IDs dentro do intervalo de datas
filtered_ids = [row[0] for row in filtered_data]

# Controle de seleção de ID, novo status e botão de atualização
st.write("Selecione o ID para atualizar o status:")
selected_id = st.selectbox("", filtered_ids)
novo_status = st.selectbox("Selecione o novo status:", ["Aguardando Entrada", "Liberar Entrada", "Descarregando", "Carregando", "Finalizado", "Inativo"])

# Botão para atualizar o status
if st.button("Atualizar Status"):
    atualizar_status(selected_id, novo_status)
    st.success(f"Status atualizado para {novo_status}")

# Exibir a tabela completa com todas as colunas
st.write("Tabela completa:")

# Estilização da tabela com cores diferentes para cada Status
table_style = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@100;300;500;700&family=Roboto:ital,wght@0,300;1,300&display=swap');
* {
  font-family: 'Roboto', sans-serif;
}

table {
  border-collapse: collapse;
  width: 100%;
}

th, td {
  padding: 8px;
  text-align: left;
  border: 1px solid #ddd;
}

th {
  background-color: #f5f5f5;
}

tr:hover {
  background-color: #f0f0f0;
}

</style>
"""

# Adicionar estilização da tabela
st.write(table_style, unsafe_allow_html=True)

# Criar uma tabela compacta
table = "<table>"
table += "<thead><tr>"
for col_name in column_names:
    table += f"<th>{col_name}</th>"
table += "</tr></thead><tbody>"

# Exibir os dados filtrados na tabela com cores diferentes para cada Status
for row in filtered_data:
    row_class = status_colors.get(row[2], "")  # Obtém a cor com base no Status
    table += f"<tr style='background-color:{row_class}'>"
    for value in row:
        table += f"<td>{value}</td>"
    table += "</tr>"
table += "</tbody></table>"

# Exibir a tabela no Streamlit
st.write(table, unsafe_allow_html=True)


