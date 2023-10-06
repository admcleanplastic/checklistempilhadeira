# gestao_entrada.py

import streamlit as st
import sqlite3
from datetime import datetime

# Função para atualizar o status no banco de dados
def atualizar_status(selected_id, novo_status):
    conn = sqlite3.connect('novo.db')
    cursor = conn.cursor()
    update_query = "UPDATE entrada SET Status = ? WHERE ID = ?"
    cursor.execute(update_query, (novo_status, selected_id))
    conn.commit()
    conn.close()

def main():
    st.title('Gestão de Entradas')
    with open("visualizacao.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

    conn = sqlite3.connect('novo.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM entrada")
    data = cursor.fetchall()
    column_names = [description[0] for description in cursor.description]
    conn.close()

    # Filtra as linhas onde o Status não é "Inativo"
    filtered_data = [list(row) for row in data if row[column_names.index("Status")] != "Inativo"]

    # Substitua "None" por "Aguardando Ação" na coluna "Status"
    for row in filtered_data:
        if row[column_names.index("Status")] is None:
            row[column_names.index("Status")] = "Aguardando Ação"

    unique_statuses = list(set([row[column_names.index("Status")] for row in filtered_data]))
    unique_statuses.append("Inativo")  # Adicionei "Inativo" à lista de status

    unique_locais = list(set([row[column_names.index("local_entrada")] for row in filtered_data]))

    selected_status = st.selectbox("Filtrar por status:", ["Todos"] + unique_statuses)
    selected_local = st.selectbox("Filtrar por Local de Entrada:", ["Todos"] + unique_locais)

    # Filtra os dados com base nas seleções feitas pelo usuário
    if selected_status != "Todos":
        filtered_data = [row for row in filtered_data if row[column_names.index("Status")] == selected_status]

    if selected_local != "Todos":
        filtered_data = [row for row in filtered_data if row[column_names.index("local_entrada")] == selected_local]

    unique_motivo = list(set([row[column_names.index("motivo")] for row in filtered_data]))
    selected_motivo = st.selectbox("Filtrar por Motivo:", ["Todos"] + unique_motivo)

    if selected_motivo != "Todos":
        filtered_data = [row for row in filtered_data if row[column_names.index("motivo")] == selected_motivo]

    data_atual = datetime.now().strftime('%Y-%m-%d')
    filtered_data = [row for row in filtered_data if row[column_names.index("data")] == data_atual]

    col1, col2 = st.columns(2)
    with col1:
        selected_id = st.selectbox("Para atualizar, selecione o ID:", [str(row[0]) for row in filtered_data])
    with col2:
        novo_status = st.selectbox("Selecione o novo status:", ['Liberar Entrada', 'Descarregando', 'Carregando', 'Operação Finalizada'])

    if st.button('Atualizar'):
        atualizar_status(selected_id, novo_status)

    table = "<style>tbody tr:nth-of-type(odd) {background-color: #f5f5f5;}</style>"
    table += "<table><thead><tr>"
    for col_name in column_names:
        table += f"<th>{col_name}</th>"
    table += "</tr></thead><tbody>"

    for row in filtered_data:
        status = row[column_names.index("Status")]
        if status == "Operação Finalizada":
            table += "<tr style='background-color: green; color: white;'>"
        elif status == "Liberar Entrada":
            table += "<tr style='background-color: yellow;'>"
        elif status == "Carregando":
            table += "<tr style='background-color: lightblue;'>"
        elif status == "Descarregando":
            table += "<tr style='background-color: #0FC2C0;'>"
        else:
            table += "<tr>"
        for value in row:
            table += f"<td>{value}</td>"
        table += "</tr>"
    table += "</tbody></table>"

    st.write(table, unsafe_allow_html=True)

    # Retorna a variável column_names
    return column_names

if __name__ == '__main__':
    main()
