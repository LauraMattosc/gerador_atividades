import streamlit as st
from api_requests import call_api

def generate_prompt_for_analysis(data):
    """
    Gera um prompt detalhado para análise estratégica e objetiva dos alunos da turma.

    Parâmetros:
    data (DataFrame): Dados da turma.

    Retorna:
    str: Prompt gerado a partir dos dados da turma.
    """
    prompt = (
        "Você é um especialista em análise de dados educacionais. Analise os dados abaixo da turma selecionada e forneça uma análise com as seguintes características:\n"
        "- Três dicas super curtas e numeradas sobre a turma, em português.\n"
        "- As dicas devem ser claras e úteis para professores, abordando características gerais da turma e recomendações práticas.\n"
        "- Inclua observações que sintetizem informações agregadas (como padrões gerais ou tendências).\n"
        "- Destaque algum aluno que seja um outlier, mencionando brevemente sua característica distintiva.\n"
        "- Apresente as dicas em formato de lista numerada. Exemplo de formatação desejada:\n"
        "  1. A turma apresenta uma boa diversidade de hipóteses de leitura, o que sugere uma abordagem pedagógica flexível.\n"
        "  2. Alguns alunos, como [nome do aluno], mostram uma evolução significativa em suas hipóteses de leitura, indicando uma adaptação bem-sucedida ao currículo.\n"
        "  3. Uma porcentagem relevante dos alunos mantém hipóteses estáveis, sugerindo a necessidade de reforço em determinadas áreas.\n"
        "\nAgora, analise os dados a seguir e siga o formato de saída indicado:\n\n"
        f"{data.to_string(index=False)}"
    )
    return prompt



def analyze_data(data):
    st.write("Gerando análise dos dados da turma...")
    prompt = generate_prompt_for_analysis(data)
    response = call_api(prompt)
    return response