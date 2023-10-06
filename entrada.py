import sqlite3
import csv
import streamlit as st
from datetime import date

st.title("Inclusão de Operador")

# Data de entrada não pode ser alterada!
data = st.date_input("Data", value=date.today(), key="data")


Empresa = st.selectbox('Empresa', ['Clean Plastic'])

col1, col2 = st.columns(2)
with col1:
    Nome_completo = st.text_input("Nome Completo:").upper()
    user = st.text_input("Usuário").upper()
    Turno = st.selectbox('Turno:', ['1º Turno','2º Turno,'3º Turno','ADM'])
    
    
    
    

with col2:
      Setor = st.selectbox('Setor:', ['Blenda','Recebimento','Logística'])
      password = st.text_input('Senha', type='password')
      Equipamento = st.selectbox('Equipamento:', ['Empilhadeira Recevimento 01'])
    



def is_form_valid(data, nome_completo, tipo_veiculo, motivo, placa, razao_social, estado, cidade, telefone, frete_retorno, local_entrada, status_veiculo, numero_page):
    required_fields = [
        data,
        nome_completo,
        tipo_veiculo,
        motivo,
        placa,
        razao_social,
        estado,
        cidade,
        telefone,
        frete_retorno,
        local_entrada,
        status_veiculo,
        numero_page,
    ]

    for field in required_fields:
        if not field:
            return False

    return True

if st.button("Salvar"):
    if is_form_valid(data, nome_completo, tipo_veiculo, motivo, placa, razao_social, estado, cidade, telefone, frete_retorno, local_entrada, status_veiculo, numero_page):
        # Conectar ao banco de dados ou criar um novo se ele não existir
        conn = sqlite3.connect('novo.db')

        # Criar um objeto cursor para executar consultas SQL
        cursor = conn.cursor()

        # Criar a tabela 'entrada' se ela não existir com o campo "Local de Entrada"
        cursor.execute('''CREATE TABLE IF NOT EXISTS entrada (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        data TEXT,
                        local_entrada TEXT,
                        estado TEXT,
                        cidade TEXT,
                        razao_social TEXT,
                        motivo TEXT,
                        tipo_veiculo TEXT,
                        frete_retorno TEXT,
                        status_veiculo TEXT,
                        placa TEXT,
                        nome_completo TEXT,
                        telefone TEXT,
                        info_complementar TEXT,
                        status TEXT,
                        numero_page INTEGER
                    )''')

        # Obter os valores dos campos
        data_value = data.strftime("%Y-%m-%d")
        local_entrada_value = local_entrada
        estado_value = estado
        cidade_value = cidade
        razao_social_value = razao_social
        motivo_value = motivo
        tipo_veiculo_value = tipo_veiculo
        frete_retorno_value = frete_retorno
        status_veiculo_value = status_veiculo
        placa_value = placa
        nome_completo_value = nome_completo
        telefone_value = telefone
        info_complementar_value = info_complementar
        status_value = status
        numero_page_value = numero_page

        # Inserir os valores na tabela 'entrada'
        cursor.execute('''INSERT INTO entrada (
                        data,
                        local_entrada,
                        estado,
                        cidade,
                        razao_social,
                        motivo,
                        tipo_veiculo,
                        frete_retorno,
                        status_veiculo,
                        placa,
                        nome_completo,
                        telefone,
                        info_complementar,
                        status,
                        numero_page
                    )
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                   (
                       data_value,
                       local_entrada_value,
                       estado_value,
                       cidade_value,
                       razao_social_value,
                       motivo_value,
                       tipo_veiculo_value,
                       frete_retorno_value,
                       status_veiculo_value,
                       placa_value,
                       nome_completo_value,
                       telefone_value,
                       info_complementar_value,
                       status_value,
                       numero_page_value,
                   ))

        # Confirmar as alterações e fechar a conexão
        conn.commit()
        conn.close()
        st.success("Dados salvos com sucesso!")
    else:
        st.warning("Preencha todos os campos antes de salvar.")
