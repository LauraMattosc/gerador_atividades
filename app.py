import streamlit as st
import pandas as pd
import datetime
import matplotlib.pyplot as plt
from api_requests import call_api  # Importando a função renomeada
from prompt_dicas import generate_prompt_for_analysis
from prompt_aula import generate_prompt_for_activity
import logging

# Configuração da interface do Streamlit
st.set_page_config(page_title="Painel da Classe e Gerador de Aulas", layout="wide")

# Verificação da chave da API
st.write("Debug: Verificando a chave da API diretamente.")
try:
    st.write("API key:", st.secrets["groq_api_key"])  # Apenas para verificar se a chave é acessível
except KeyError as e:
    st.write(f"Erro: {e}")

# Configuração do logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def configure_ui():
    st.title('📊 Painel da Classe e Gerador de Aulas')

# Funções de captura de entradas e exibição de dados da turma mantidas

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

# Função para exibir dados da turma

# Função para exibir dados da turma
def display_class_data(data: pd.DataFrame, turma: str):
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
        return color_map.get(val, "#FFFFFF")

    # Aplicando as cores com Styler.format() para a coluna de hipóteses
    styled_data = data[['student_name', 'hypothesis_name']].style.applymap(
        lambda x: f'background-color: {highlight_hypothesis(x)}', subset=['hypothesis_name']
    )

    st.dataframe(styled_data, width=1000)



# Função para analisar os dados da turma e fornecer dicas

def analyze_class_data(data):
    prompt = generate_prompt_for_analysis(data)
    logger.info(f"Prompt gerado para análise: {prompt}")
    tips = call_api(prompt, model="llama2-70b-4096")  # Usando call_api genérico
    if tips:
        logger.info(f"Resposta da API para dicas: {tips}")
    else:
        logger.error("❌ O retorno da API foi nulo ou vazio para as dicas.")
    return tips

# Função para gerar plano de aula

def generate_lesson_plan(componente, unidade_tematica, objetivo_conhecimento, current_month, perfis_turma):
    prompt = generate_prompt_for_activity(
        componente,
        unidade_tematica,
        objetivo_conhecimento,
        current_month,
        perfis_turma
    )
    logger.info(f"Prompt gerado para o plano de aula: {prompt}")
    plano_aula = call_api(prompt, model="llama2-90b-4096")  # Usando call_api genérico
    if plano_aula:
        logger.info("Plano de aula gerado com sucesso pela IA.")
    else:
        logger.error("❌ O retorno da API foi nulo ou vazio. Verifique o prompt e a resposta.")
    return plano_aula

# Função principal

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
                perfis_turma = "Perfil detalhado da turma aqui."  # Ajustar conforme necessidade
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
                    st.markdown("### ❗ **Detalhes do Erro**")
                    st.markdown(
                        f"""
                        - **🧩 Componente:** {componente}
                        - **📚 Unidade Temática:** {unidade_tematica}
                        - **🎯 Objetivo:** {objetivo_conhecimento}
                        - **📝 Prompt:** Erro ao processar
                        """
                    )
            except Exception as e:
                st.error(f"Erro ao gerar o plano: {str(e)}")
                st.markdown("### ❗ **Detalhes do Erro**")
                st.markdown(
                    f"""
                    - **🧩 Componente:** {componente}
                    - **📚 Unidade Temática:** {unidade_tematica}
                    - **🎯 Objetivo:** {objetivo_conhecimento}
                    - **❌ Erro:** {str(e)}
                    """
                )
                logger.error(f"Erro ao gerar o plano: {str(e)}")


if __name__ == "__main__":
        main()
