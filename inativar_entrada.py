import streamlit as st
import sqlite3
from datetime import date, timedelta

st.title('Inativar Entrada')

# Função para inativar um registro no banco de dados
def inativar_registro(id):
    conn = sqlite3.connect('novo.db')
    cursor = conn.cursor()
    cursor.execute("UPDATE entrada SET Status='Inativo' WHERE ID=?", (id,))
    conn.commit()
    conn.close()

# Conectar ao banco de dados
conn = sqlite3.connect('novo.db')
cursor = conn.cursor()

# Criar componentes de seleção de data
start_date = st.date_input("Selecione a data de início:", date.today() - timedelta(days=30))
end_date = st.date_input("Selecione a data de término:", date.today())

# Executar a consulta SQL para obter os dados da tabela 'entrada' dentro do intervalo de datas selecionado
cursor.execute("SELECT * FROM entrada WHERE DATE(data) >= ? AND DATE(data) <= ?", (start_date, end_date))
data = cursor.fetchall()

# Obter os nomes das colunas
column_names = [description[0] for description in cursor.description]

# Fechar a conexão com o banco de dados
conn.close()

# Criar uma tabela no Streamlit
table = "<style>tbody tr:nth-of-type(odd) {background-color: #f5f5f5;}</style>"
table += "<table><thead><tr>"
for col_name in column_names:
    table += f"<th>{col_name}</th>"
table += "</tr></thead><tbody>"

# Exibir os dados na tabela
for row in data:
    table += "<tr>"
    for value in row:
        table += f"<td>{value}</td>"
    table += "</tr>"
table += "</tbody></table>"

# Exibir a tabela no Streamlit
st.write(table, unsafe_allow_html=True)

# Seletor de ID para inativar
selected_id = st.selectbox("Para inativar, selecione o ID:", [str(row[0]) for row in data])
if st.button('Inativar'):
    inativar_registro(selected_id)



