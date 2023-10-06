import streamlit as st
import sqlite3
from datetime import date, timedelta

st.title('Atualizar Status de Entrada')

# Função para atualizar o status de um registro pelo ID
def atualizar_status(selected_ids, novo_status):
    if selected_ids:
        conn = sqlite3.connect('novo.db')
        cursor = conn.cursor()
        cursor.executemany("UPDATE entrada SET Status=? WHERE ID=?", [(novo_status, id) for id in selected_ids])
        conn.commit()
        conn.close()
        st.success("Status atualizado com sucesso!")
    else:
        st.warning("Selecione pelo menos um ID para atualizar o status.")

# Conectar ao banco de dados
conn = sqlite3.connect('novo.db')
cursor = conn.cursor()

# Criar componentes de seleção de data
start_date = st.date_input("Selecione a data de início:", date.today())
end_date = st.date_input("Selecione a data de término:", date.today())

# Executar a consulta SQL para obter os dados da tabela 'entrada' dentro do intervalo de datas selecionado
cursor.execute("SELECT * FROM entrada WHERE DATE(data) >= ? AND DATE(data) <= ?", (start_date, end_date))
data = cursor.fetchall()

# Obter os nomes das colunas
column_names = [description[0] for description in cursor.description]

# Filtros
col1, col2, col3, col4 = st.columns(4)
with col1:
    emp_origem_filter = st.selectbox("Empresa de origem:", ["Todos"] + list(set(row[5] for row in data)))

with col2:
    motivo_filter = st.selectbox("Motivo da entrada:", ["Todos"] + list(set(row[6] for row in data)))

with col3:
    local_entrada_filter = st.selectbox("Local de entrada:", ["Todos"] + list(set(row[2] for row in data)))

with col4:
    status_filter = st.selectbox("Status:", ["Todos"] + list(set(row[14] for row in data)))

# Aplicar filtros
filtered_data = []
for row in data:
    if (emp_origem_filter == "Todos" or row[5] == emp_origem_filter) and \
       (motivo_filter == "Todos" or row[6] == motivo_filter) and \
       (local_entrada_filter == "Todos" or row[2] == local_entrada_filter) and \
       (status_filter == "Todos" or row[14] == status_filter) and \
       (row[column_names.index("status")] != "Inativo"):
        filtered_data.append(row)

# Substituir "None" por "Aguardando Entrada" na coluna "Status"
filtered_data = [[value if value is not None else "Aguardando Entrada" for value in row] for row in filtered_data]

# Fechar a conexão com o banco de dados
conn.close()

# Criar uma tabela no Streamlit usando filtered_data
table = "<style>tbody tr:nth-of-type(odd) {background-color: #f5f5f5;}</style>"
table += "<table><thead><tr>"
for col_name in column_names:
    table += f"<th>{col_name}</th>"
table += "</tr></thead><tbody>"

# Exibir os dados na tabela
for row in filtered_data:
    if row[column_names.index("status")] == "Descarregamento Finalizado":
         table += "<tr style='background-color: #8FBC8F;'>"
    elif row[column_names.index("status")] == "Aguardando Entrada":
        table += "<tr style='background-color: #FF6347;'>"
    elif row[column_names.index("status")] == "Carregamento Finalizado":
        table += "<tr style='background-color: #3CB371;'>" 
    elif row[column_names.index("status")] == "Liberar Entrada":
       table += "<tr style='background-color: #F0E68C;'>"
    elif row[column_names.index("status")] == "Carregando":
       table += "<tr style='background-color: #6495ED;'>"  
    elif row[column_names.index("status")] == "Descarregando":
       table += "<tr style='background-color: #1E90FF;'>"
    for value in row:
        table += f"<td>{value}</td>"
    table += "</tr>"

table += "</tbody></table>"

# Exibir a tabela no Streamlit
st.write(table, unsafe_allow_html=True)

# Seletor de IDs para atualizar o status
selected_ids = st.multiselect("Selecione os IDs para atualizar o status:", [str(row[0]) for row in filtered_data])

# Seletor de novo status
novo_status = st.selectbox("Novo Status:", ["Aguardando Entrada", "Liberar Entrada", "Carregando", "Descarregando", "Descarregamento Finalizado", "Carregamento Finalizado"])

# Botão para atualizar o Status
if st.button("Atualizar Status"):
    atualizar_status(selected_ids, novo_status)
