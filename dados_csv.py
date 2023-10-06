import sqlite3
from datetime import datetime
import csv

def atualizar_status(id, novo_status):
    conn = sqlite3.connect('novo.db')
    cursor = conn.cursor()
    cursor.execute("UPDATE entrada SET Status=? WHERE ID=?", (novo_status, id))
    conn.commit()

    csv_data = []
    cursor.execute("SELECT * FROM entrada")
    data = cursor.fetchall()
    for row in data:
        csv_data.append(row)

    with open(csv_filename, 'w', newline='') as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(column_names)
        csv_writer.writerows(csv_data)

    conn.close()

def main():
    conn = sqlite3.connect('novo.db')
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM entrada")
    data = cursor.fetchall()

    column_names = [description[0] for description in cursor.description]

    conn.close()

    unique_statuses = list(set([row[column_names.index("Status")] for row in data]))
    selected_status = st.selectbox("Filtrar por status:", ["Todos"] + unique_statuses)
    filtered_data = data
    if selected_status != "Todos":
        filtered_data = [row for row in filtered_data if row[column_names.index("Status")] == selected_status]

    # Restante do seu código...

if __name__ == '__main__':
    import streamlit as st

    st.title('Gestao Entradas')
    with open("visualizacao.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

    csv_filename = "dados_exportados.csv"
    
    # Chame a função principal
    main()
