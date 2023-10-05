import streamlit as st

st.title("Checklist para Empilhadeira")

# Defina os itens do checklist
itens_checklist = [
    "Nível de água do Radiador",
    "Nível de óleo do Motor",
    "Nível de óleo da transmissão",
    "Nível de óleo do Sistema Hidráulico",
    "Comandos Hidráulicos funcionando corretamente",
    "Painel de instrumentos funcionando corretamente",
    "Garfos e travas em condições",
    "Sistema de freio em condições",
    "A condição das mangueiras e abraçadeiras estão ok",
    "Verificação da pressão e condições do pneus, desgastes e porcas apertadas",
    "Faróis e lanternas funcionando corretamente",
    "Luz e alarme de ré funcionando corretamente",
    "Buzina funcionando",
    "Cinto de Segurança",
    "Extintor de incêndio (vencimento e conservação)",
    "Existem vazamentos aparentes (água, óleo ou combustível)",
    "Sistema de direção funcionando corretamente",
    "Motor rateando, barulhento e/ou com vazamento",
    "Sistema de elevação e abaixamento com folga, deslocamento excessivo, vibrações, vazamentos e mangueiras soltas",
    "Conexões soltas e/ou sujeira na bateria",
    "Retrovisores em bom estado (quando aplicável)",
    "Horímetro inicial",
    "Horímetro final"
]

# Crie uma lista para armazenar o status (OK ou NOK) de cada item
status_itens = []

# Crie um loop para exibir cada item do checklist e permitir que o usuário selecione OK ou NOK
for item in itens_checklist:
    st.write(item)
    status = st.radio(f"Selecione o status para {item}:", ("OK", "NOK"))
    status_itens.append((item, status))

# Exiba o resumo do checklist
st.title("Resumo do Checklist")
for item, status in status_itens:
    st.write(f"{item}: {status}")

