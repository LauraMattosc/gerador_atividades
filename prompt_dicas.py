import streamlit as st
from api_requests import call_api

def generate_prompt_for_analysis(data):
    """
    Gera um prompt para análise estratégica e objetiva dos alunos da turma.

    Parâmetros:
    data (DataFrame): Dados da turma.

    Retorna:
    str: Prompt gerado a partir dos dados da turma.
    """
    prompt = (
        "Analise os seguintes dados da turma e forneça dicas curtas, em português, no máximo 3, "
        "elas devem ser sobre a turma selecionada:\n\n"
        f"{data.to_string(index=False)}"
    )
    return prompt

def analyze_data(data):
    st.write("Gerando análise dos dados da turma...")
    prompt = generate_prompt_for_analysis(data)
    response = call_api(prompt)
    return response