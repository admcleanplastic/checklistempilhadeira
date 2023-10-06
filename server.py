import sqlite3
import streamlit as st
import pandas as pd

st.title("Gerenciar Entradas")

# Conectar ao banco de dados
conn = sqlite3.connect('novo.db')
cursor = conn.cursor()

# Função para listar todos os registros
def listar_registros():
    cursor.execute("SELECT * FROM entrada")
    registros = cursor.fetchall()
    return registros

# Carregar os registros em um DataFrame Pandas
registros = listar_registros()
df = pd.DataFrame(registros, columns=["ID", "Data", "Local Entrada", "Estado", "Cidade", "Razão Social", "Motivo", "Tipo Veículo", "Frete Retorno", "Status Veículo", "Placa", "Nome Completo", "Telefone", "Info Complementar", "Status", "Número Page"])

# Exibir os registros em uma tabela Pandas
st.write(df)

# Opções para editar e excluir registros
opcao = st.selectbox("Selecione uma opção:", ["Editar", "Excluir"])

if opcao == "Editar":
    st.subheader("Editar Registro")
    id_registro = st.number_input("ID do Registro para Edição", min_value=1, max_value=len(df))

    if st.button("Carregar Registro"):
        registro_selecionado = df.iloc[id_registro - 1]
        st.write("Registro Selecionado:")
        st.write(registro_selecionado)

        # Interface para editar os campos
        novo_valor = st.text_input("Novo Valor")
        coluna_para_editar = st.selectbox("Selecione a Coluna para Editar", df.columns)
        
        if st.button("Aplicar Edição"):
            df.at[id_registro - 1, coluna_para_editar] = novo_valor
            st.success("Edição aplicada com sucesso!")

            # Atualizar o registro no banco de dados
            cursor.execute(f"UPDATE entrada SET {coluna_para_editar} = ? WHERE ID = ?", (novo_valor, id_registro))
            conn.commit()

elif opcao == "Excluir":
    st.subheader("Excluir Registro")
    id_registro = st.number_input("ID do Registro para Excluir", min_value=1, max_value=len(df))

    if st.button("Excluir Registro"):
        df.drop(index=id_registro - 1, inplace=True)
        st.warning("Registro excluído com sucesso!")

        # Excluir o registro do banco de dados
        cursor.execute("DELETE FROM entrada WHERE ID = ?", (id_registro,))
        conn.commit()

# Fechar a conexão com o banco de dados
conn.close()
