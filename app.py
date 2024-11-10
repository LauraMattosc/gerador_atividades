import streamlit as st
import pandas as pd
import datetime
import matplotlib.pyplot as plt
from api_requests import call_api  # Importando a função da API
from prompt_dicas import generate_prompt_for_analysis
from prompt_aula import generate_prompt_for_activity
import logging

# Configuração da interface do Streamlit
st.set_page_config(page_title="Painel da Classe e Gerador de Aulas", layout="wide")

# Configuração do logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def configure_ui():
    st.title('📊 Painel da Classe e Gerador de Aulas')

def get_user_inputs(data):
    """Captura as entradas de dados do usuário."""
    st.sidebar.header("Configurações da Atividade")
    turmas = data['class_name'].unique()
    turma = st.sidebar.selectbox("Escolha a turma:", turmas)
    componente = st.sidebar.selectbox("Escolha o componente:", ["Matemática", "Língua Portuguesa", "Escrita Compartilhada e Autônoma"])
    unidade_tematica = st.sidebar.selectbox("Escolha a unidade temática:", ["Leitura", "Escrita", "Produção de Texto"])
    objetivos_map = {
        "Leitura": ["Compreensão em Leitura"],
        "Escrita": ["Produção de Textos"],
        "Oralidade": ["Contação de Histórias"]
    }
    objetivo_conhecimento = st.sidebar.selectbox("Objetivo de Conhecimento", objetivos_map[unidade_tematica])
    
    return turma, componente, unidade_tematica, objetivo_conhecimento

def display_class_data(data: pd.DataFrame, turma: str):
    """Exibe os dados da turma, como gráfico e tabela de hipóteses."""
    data = data[data['class_name'] == turma]
    st.subheader("Porcentagem de Alunos por Hipótese")
    hypothesis_counts = data['hypothesis_name'].value_counts(normalize=True) * 100
    labels = hypothesis_counts.index
    sizes = hypothesis_counts.values
    colors = ['#86E085', '#C8FFBB', '#FFF6A1', '#FFC9A3', '#FFA9B8', '#FFFFFF']

    fig1, ax1 = plt.subplots(figsize=(5, 3))
    wedges, texts, autotexts = ax1.pie(sizes, autopct='%1.1f%%', startangle=70, colors=colors)
    ax1.legend(wedges, labels, title="Hipóteses", loc="center left", bbox_to_anchor=(1, 0, 0.2, 1), prop={'size': 8})
    plt.setp(autotexts, size=8)
    plt.tight_layout()
    st.pyplot(fig1)

    st.subheader('Tabela de Alunos por Hipótese')
    color_map = {
        'Alfabética': '#86E085',
        'Silábico-alfabética': '#C8FFBB',
        'Silábica c/ valor': '#FFF6A1',
        'Silábica s/ valor': '#FFC9A3',
        'Pré-silábica': '#FFA9B8'
    }

    def highlight_hypothesis(val):
        color = color_map.get(val, "#FFFFFF")
        return f'background-color: {color}'

    styled_data = data.style.apply(
        lambda x: [highlight_hypothesis(v) for v in x], subset=['hypothesis_name']
    )
    st.dataframe(styled_data, width=1000)

def clean_response(response: str) -> str:
    """
    Limpa a resposta da API removendo quebras de linha e múltiplos espaços.
    """
    cleaned_response = response.replace('\n', ' ').replace('\r', '').strip()
    cleaned_response = ' '.join(cleaned_response.split())
    return cleaned_response

def format_tips_as_html(tips: str) -> str:
    """
    Formata as dicas como uma lista não ordenada (HTML), onde cada dica é um item da lista.
    
    Parâmetros:
    tips (str): Dicas em formato de string. Cada dica pode ser separada por uma quebra de linha.
    
    Retorna:
    str: Dicas formatadas como lista HTML.
    """
    # Divida as dicas por linha e remova linhas vazias ou espaços extras
    dicas = [dica.strip() for dica in tips.split("\n") if dica.strip()]
    
    # Inicia a lista HTML
    formatted_tips = "<ul>"
    
    # Adiciona cada dica como um item de lista <li>
    for dica in dicas:
        formatted_tips += f"<li>{dica}</li>"
    
    # Fecha a lista HTML
    formatted_tips += "</ul>"
    
    return formatted_tips

def analyze_class_data(data):
    """
    Analisa os dados da turma e retorna dicas formatadas.
    """
    prompt = generate_prompt_for_analysis(data)
    logger.info(f"Prompt gerado para análise: {prompt}")
    tips = call_api(prompt, model="llama3-8b-8192")
    if tips:
        logger.debug(f"Resposta da API (antes de limpar): {repr(tips)}")
        cleaned_response = clean_response(tips)
        formatted_tips = format_tips_as_html(cleaned_response)  # Formata como HTML
        logger.debug(f"Resposta da API (depois de limpar e formatar): {repr(formatted_tips)}")
        return formatted_tips
    else:
        logger.error("❌ O retorno da API foi nulo ou vazio.")
        return "Nenhuma dica foi retornada."

def generate_lesson_plan(componente, unidade_tematica, objetivo_conhecimento, current_month, perfis_turma):
    """
    Gera e formata o plano de aula com base nos dados fornecidos.
    """
    prompt = generate_prompt_for_activity(
        componente,
        unidade_tematica,
        objetivo_conhecimento,
        current_month,
        perfis_turma
    )
    logger.info(f"Prompt gerado para o plano de aula: {prompt}")
    plano_aula = call_api(prompt, model="llama3-8b-8192")
    if plano_aula:
        formatted_plan = format_lesson_plan(clean_response(plano_aula))
        logger.info("Plano de aula gerado com sucesso pela IA.")
        return formatted_plan
    else:
        logger.error("❌ O retorno da API foi nulo ou vazio. Verifique o prompt e a resposta.")
        return "Não foi possível gerar o plano de aula. Verifique os dados e tente novamente."

def format_lesson_plan(plan: str) -> str:
    """
    Formata o plano de aula em Markdown com seções e listas bem definidas.
    """
    formatted_plan = plan.replace("\n", " ").replace("\r", "").strip()
    formatted_plan = ' '.join(formatted_plan.split())
    formatted_plan = formatted_plan.replace("# Plano de Aula", "\n# Plano de Aula")
    formatted_plan = formatted_plan.replace("## ", "\n\n## ").replace("### ", "\n\n### ")
    formatted_plan = formatted_plan.replace("- ", "\n- ")
    return formatted_plan

def main():
    configure_ui()

    try:
        data = pd.read_csv('dados.csv')
    except Exception as e:
        st.error(f"Erro ao carregar os dados do CSV: {e}")
        logger.error(f"Erro ao carregar dados: {e}")
        return

    turma, componente, unidade_tematica, objetivo_conhecimento = get_user_inputs(data)

    st.subheader("Resumo Estratégico")
    hypothesis_counts = data['hypothesis_name'].value_counts(normalize=True) * 100
    for hypothesis, percentage in hypothesis_counts.items():
        st.write(f"- **{hypothesis}:** {percentage:.1f}%")

    try:
        tips = analyze_class_data(data)
        if tips:
            st.markdown(
                f"""
                <div style="background-color:#f0f8ff; padding:15px; border-radius:10px;">
                <h3 style="color:#2a9d8f;">💡 Dicas da IA 🦙:</h3>
                <p style="font-size:16px; color:#264653;">{tips}</p>
                </div>
                """,
                unsafe_allow_html=True
            )
        else:
            st.warning("Nenhuma dica foi retornada pela API.")
    except Exception as e:
        st.error(f"Erro ao analisar os dados com a IA: {e}")
        logger.error(f"Erro ao analisar os dados com a IA: {e}")

    tab_dados, tab_atividade = st.tabs(["📊 Dados da Classe", "📝 Gerar Aula"])

    with tab_dados:
        display_class_data(data, turma)

    with tab_atividade:
        if st.button("Gerar Aula"):
            try:
                current_month = datetime.datetime.now().strftime("%B de %Y")
                perfis_turma = "Perfil detalhado da turma aqui."
                plano_aula = generate_lesson_plan(componente, unidade_tematica, objetivo_conhecimento, current_month, perfis_turma)
                if plano_aula:
                    st.markdown(
                        f"""
                        <div style="background-color:#ffffff; padding:20px; border-radius:10px; border:1px solid #e0e0e0;">
                        {plano_aula}
                        </div>
                        """,
                        unsafe_allow_html=True
                    )

                    col1, col2, col3 = st.columns(3)
                    with col1:
                        if st.button("📥 Baixar PDF"):
                            st.info("Funcionalidade de download em desenvolvimento")
                    with col2:
                        if st.button("✏️ Editar Plano"):
                            st.info("Funcionalidade de edição em desenvolvimento")
                    with col3:
                        if st.button("💾 Salvar"):
                            st.info("Funcionalidade de salvamento em desenvolvimento")
                else:
                    st.error("❌ Não foi possível gerar o plano de aula. Tente novamente.")
            except Exception as e:
                st.error(f"Erro ao gerar o plano: {str(e)}")

if __name__ == "__main__":
    main()
