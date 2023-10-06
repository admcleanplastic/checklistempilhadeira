import sqlite3
import streamlit as st

st.title("Gerenciar Entradas")

# Conectar ao banco de dados
conn = sqlite3.connect('novo.db')
cursor = conn.cursor()

# Função para listar todos os registros
def listar_registros():
    cursor.execute("SELECT * FROM entrada")
    registros = cursor.fetchall()
    return registros

# Função para editar um registro
def editar_registro(registro):
    data, local_entrada, estado, cidade, razao_social, motivo, tipo_veiculo, frete_retorno, status_veiculo, placa, nome_completo, telefone, info_complementar, status, numero_page, id = registro

    # Exibir os campos na interface para edição
    data = st.date_input("Data Entrada", value=data)
    local_entrada = st.selectbox('Local de entrada', ['Clean Plastic', 'Clean Poa', 'Clean Jundiai', 'Clean Bottle', 'Clean Fortal', 'Raposo Plasticos', 'Raposo Minas', 'Fornecedor PF', 'Outro'], index=local_entrada)
    estado = st.selectbox('Selecione o estado', estados, index=estados.index(estado))
    cidade = st.selectbox('Selecione a cidade', municipios, index=municipios.index(cidade))
    razao_social = st.text_input('Razão Social', razao_social)
    motivo = st.selectbox('Motivo:', ['Carregar', 'Descarregar', 'Entrega', 'Retirada'], index=motivo)
    tipo_veiculo = st.selectbox('Tipo de Veiculo:', ["Truck-Side", "Carreta-Side", "Truck-Grade Baixa", "Carreta-Grade Baixa", "Carreta Graneleira", "Container","Bitrem","Bitruck"], index=tipo_veiculo)
    placa = st.text_input('Placa do Veiculo', placa).upper()
    nome_completo = st.text_input("Nome Completo", nome_completo).upper()
    telefone = st.text_input('Telefone', telefone).upper()
    frete_retorno = st.selectbox('Possuem Frete Retorno?', ['Sim', 'Nao'], index=frete_retorno)
    numero_page = st.number_input('Número do Page', min_value=1, max_value=16, step=1, value=numero_page)
    info_complementar = st.text_area('Info. Complementar', info_complementar)

    # Botão para atualizar o registro
    if st.button("Atualizar"):
        cursor.execute('''UPDATE entrada SET data=?, local_entrada=?, estado=?, cidade=?, razao_social=?, motivo=?, tipo_veiculo=?, frete_retorno=?, status_veiculo=?, placa=?, nome_completo=?, telefone=?, info_complementar=?, numero_page=? WHERE id=?''',
                       (data, local_entrada, estado, cidade, razao_social, motivo, tipo_veiculo, frete_retorno, status_veiculo, placa, nome_completo, telefone, info_complementar, numero_page, id))
        conn.commit()
        st.success("Registro atualizado com sucesso!")

    # Botão para excluir o registro
    if st.button("Excluir"):
        cursor.execute("DELETE FROM entrada WHERE id=?", (id,))
        conn.commit()
        st.warning("Registro excluído com sucesso!")

# Listar todos os registros
registros = listar_registros()

# Exibir os registros na interface
if registros:
    for registro in registros:
        st.subheader(f"Registro #{registro[0]}")
        editar_registro(registro)
else:
    st.info("Nenhum registro encontrado na tabela 'entrada'.")

# Fechar a conexão com o banco de dados
conn.close()

