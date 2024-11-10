import streamlit as st
import pandas as pd
import datetime
import matplotlib.pyplot as plt
from api_requests import call_api  # Remova qualquer referência a process_with_groq
from prompt_dicas import generate_prompt_for_analysis
from prompt_aula import generate_prompt_for_activity
import toml
import logging

# Configuração do logger para imprimir no terminal
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Configuração da interface do Streamlit
st.set_page_config(page_title="Painel da Classe e Gerador de Aulas", layout="wide")

def configure_ui():
    """Configura a interface do usuário usando o Streamlit."""
    st.title('📊 Painel da Classe e Gerador de Aulas')

# Entradas principais do usuário
def get_user_inputs(data):
    """Captura as entradas de dados do usuário.

    Retorna:
    tuple: Contendo a turma, componente, unidade temática e objetivo de conhecimento.
    """
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
def display_class_data(data, turma):
    if data is None:
        st.error("Erro ao carregar os dados da classe.")
        logger.error("Dados da classe não carregados corretamente.")
        return

    data = data[data['class_name'] == turma]
    required_columns = ['student_name', 'class_name', 'month', 'hypothesis_name']
    if not all(column in data.columns for column in required_columns):
        st.error(f"O arquivo CSV deve conter as seguintes colunas: {', '.join(required_columns)}")
        logger.error(f"Colunas ausentes no arquivo CSV. Esperado: {', '.join(required_columns)}")
        return

    st.subheader("Porcentagem de Alunos por Hipótese")
    hypothesis_counts = data['hypothesis_name'].value_counts(normalize=True) * 100
    labels = hypothesis_counts.index
    sizes = hypothesis_counts.values
    colors = ['#86E085', '#C8FFBB', '#FFF6A1', '#FFC9A3', '#FFA9B8', '#FFFFFF']

    fig1, ax1 = plt.subplots(figsize=(5, 3))
    wedges, texts, autotexts = ax1.pie(sizes, 
                                       labels=None, 
                                       autopct='%1.1f%%', 
                                       startangle=70, 
                                       colors=colors)
    ax1.legend(wedges, labels,
               title="Hipóteses",
               loc="center left",
               bbox_to_anchor=(1, 0, 0.2, 1),
               prop={'size': 8})

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
        color = color_map.get(val, '#FFFFFF')
        return f'background-color: {color}'

    styled_data = data[['student_name', 'hypothesis_name']].style.map(highlight_hypothesis, subset=['hypothesis_name'])
    st.dataframe(styled_data, width=1000)

# Função para exibir o perfil da turma
def display_class_profile(data, turma):
    if data is None:
        st.error("Erro ao carregar os dados da classe.")
        logger.error("Erro ao carregar os dados da classe para exibição de perfil.")
        return

    data = data[data['class_name'] == turma]
    hypothesis_counts = data['hypothesis_name'].value_counts()
    
    perfis_turma = ""
    for hypothesis, count in hypothesis_counts.items():
        perfis_turma += f"- **{hypothesis}:** {count} alunos\n"
    
    logger.info(f"Perfil da turma gerado: {perfis_turma}")
    return perfis_turma

# Função para analisar os dados da turma e fornecer dicas
def analyze_class_data(data):
    prompt = generate_prompt_for_analysis(data)
    logger.info(f"Prompt gerado para análise: {prompt}")  # Log para verificar o prompt
    tips = call_api(prompt)
    if tips is None:
        logger.error("❌ O retorno da API foi nulo ou vazio para as dicas.")
    else:
        logger.info(f"Resposta da API para dicas: {tips}")  # Log para verificar a resposta da API
    return tips

# Função principal para lidar com a lógica do aplicativo
def main():
    configure_ui()
  
    try:
        data = pd.read_csv('dados.csv')
        config = toml.load('credentials.toml')
        api_token = config.get("api_token", "Not found")
        groq_api_key = config.get("groq_api_key", "Not found")
    except Exception as e:
        st.error(f"Erro ao carregar os dados do CSV: {e}")
        logger.error(f"Erro ao carregar dados: {e}")
        return

    turma, componente, unidade_tematica, objetivo_conhecimento = get_user_inputs(data)

    teacher = {'name': 'Silva'}
    school = {'name': 'Escola Futuro Brilhante'}
    class_data = {'name': turma, 'year': '2023'}

    st.markdown(f"### Olá, Professora {teacher['name']}!")
    st.markdown(f"**Escola:** {school['name']}")

    current_month = datetime.datetime.now().strftime("%B de %Y")

    st.subheader("Resumo Estratégico")
    hypothesis_counts = data['hypothesis_name'].value_counts(normalize=True) * 100
    for hypothesis, percentage in hypothesis_counts.items():
        st.write(f"- **{hypothesis}:** {percentage:.1f}%")

    try:
        groq_api_key = st.secrets["api"]["groq_api_key"]
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
            st.error("❌ Erro ao processar a análise com a API Groq.")
            logger.error("❌ O retorno da API foi nulo ou vazio para as dicas.")
    except Exception as e:
        st.error(f"Erro ao analisar os dados com a IA da Llama: {e}")
        logger.error(f"Erro ao analisar os dados com a IA: {e}")

    tab_dados, tab_atividade = st.tabs(["📊 Dados da Classe", "📝 Gerar Aula"])

    with tab_dados:
        display_class_data(data, turma)
        perfis_turma = display_class_profile(data, turma)
        st.markdown(f"## Perfil da Turma\n{perfis_turma}")
    
    with tab_atividade:
        if st.button("Gerar Aula"):
            try:
                # Exibe o título do plano de aula após o botão ser pressionado
                plano_titulo = f"Plano de Aula de {componente} para o {turma}"
                st.subheader(plano_titulo)

                # Gerar o prompt inicial
                prompt = generate_prompt_for_activity(
                    componente, 
                    unidade_tematica, 
                    objetivo_conhecimento, 
                    current_month, 
                    perfis_turma
                )
                
                logger.info(f"Prompt gerado para o plano de aula: {prompt}")

                # Exibir o prompt para verificação
                with st.expander("Ver Prompt Enviado para IA"):
                    st.markdown(prompt)

                # Processar com a IA
                st.info("🤖 Gerando plano de aula personalizado...")
                plano_aula = call_api(prompt)

                # Inclua esta verificação logo após a chamada da API
                if plano_aula:
                    st.write("✅ Plano de aula gerado com sucesso!")
                    logger.info("Plano de aula gerado com sucesso pela IA.")
                else:
                    st.error("❌ O retorno da API foi nulo ou vazio. Verifique o prompt e a resposta.")
                    st.write("📝 Detalhe do Prompt:", prompt)
                    logger.warning("❌ Retorno da API vazio ou nulo.")

                # O restante do código continua abaixo
                if plano_aula:
                    # Criar tabs para diferentes visualizações do plano
                    plan_tab1, plan_tab2 = st.tabs(["📝 Plano Detalhado", "🔍 Versão Simplificada"])
                    
                    with plan_tab1:
                        st.markdown(
                            f"""
                            <div style="background-color:#ffffff; padding:20px; border-radius:10px; border:1px solid #e0e0e0;">
                            {plano_aula}
                            </div>
                            """, 
                            unsafe_allow_html=True
                        )
                        
                        # Botões de ação
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
                    
                    with plan_tab2:
                        # Versão simplificada do plano
                        st.markdown("### Resumo do Plano")
                        st.markdown(
                            f"""
                            - **Componente:** {componente}
                            - **Unidade:** {unidade_tematica}
                            - **Objetivo:** {objetivo_conhecimento}
                            - **Data:** {current_month}
                            """
                        )
                        
                        # Feedback e Avaliação
                        st.markdown("### 📊 Avalie este plano")
                        feedback = st.slider(
                            "Como você avalia este plano de aula?",
                            1, 5, 3,
                            help="1 = Precisa melhorar muito, 5 = Excelente"
                        )
                        
                        if feedback <= 3:
                            sugestoes = st.text_area(
                                "Que aspectos você gostaria de melhorar neste plano?",
                                height=100
                            )
                            if st.button("Enviar Sugestões"):
                                st.success("Obrigado pelo feedback! Suas sugestões nos ajudarão a melhorar.")
                        
                        # Área de observações
                        st.markdown("### 📝 Observações")
                        observacoes = st.text_area(
                            "Adicione suas observações sobre este plano",
                            height=150
                        )
                        if st.button("Salvar Observações"):
                            st.success("Observações salvas com sucesso!")

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
