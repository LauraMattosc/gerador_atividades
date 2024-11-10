import streamlit as st
import pandas as pd
import datetime
import matplotlib.pyplot as plt
from api_requests import fetch_activity, process_with_groq, generate_activity_with_rag
from prompt_dicas import generate_prompt_for_analysis
from prompt_aula import generate_prompt_for_activity

# Configuração da interface do Streamlit
st.set_page_config(page_title="Painel da Classe e Gerador de Atividades", layout="wide")

def configure_ui():
    """Configura a interface do usuário usando o Streamlit."""
    st.title('📊 Painel da Classe e Gerador de Atividades')

# Entradas principais do usuário
def get_user_inputs(data):
    """Captura as entradas de dados do usuário.

    Retorna:
    tuple: Contendo as credenciais da API, tema e nível de dificuldade.
    """
    st.sidebar.header("Configurações da Atividade")
    turmas = data['class_name'].unique()
    turma = st.sidebar.selectbox("Escolha a turma:", turmas)
    componente = st.sidebar.selectbox("Escolha o componente:", ["Matemática", "Língua Portuguesa"])
    unidade_tematica = st.sidebar.selectbox("Escolha a unidade temática:", ["Leitura", "Escrita", "Produção de Texto"])
    objetivo_conhecimento = st.sidebar.text_input("Objetivo de conhecimento:")
    return turma, componente, unidade_tematica, objetivo_conhecimento

# Função para buscar dados e mostrar informações da classe
def display_class_data(data, turma):
    if data is None:
        st.error("Erro ao carregar os dados da classe.")
        return

    # Filtrar dados pela turma selecionada
    data = data[data['class_name'] == turma]

    # Verificar se todas as colunas necessárias estão presentes
    required_columns = ['student_name', 'class_name', 'month', 'hypothesis_name']
    if not all(column in data.columns for column in required_columns):
        st.error(f"O arquivo CSV deve conter as seguintes colunas: {', '.join(required_columns)}")
        return

    # Gráfico de pizza de alunos alfabetizados
    st.subheader("Porcentagem de Alunos por Hipótese")
    hypothesis_counts = data['hypothesis_name'].value_counts(normalize=True) * 100
    labels = hypothesis_counts.index
    sizes = hypothesis_counts.values
    colors = ['#86E085', '#C8FFBB', '#FFF6A1', '#FFC9A3', '#FFA9B8', '#FFFFFF']

    # Ajustar para um tamanho ainda menor e mais proporcional
    fig1, ax1 = plt.subplots(figsize=(1.5, 1.25))

    # Criar o gráfico de pizza com legendas fora do gráfico
    wedges, texts, autotexts = ax1.pie(sizes, 
                                    labels=None,  # Remove as labels do gráfico
                                    autopct='%1.1f%%', 
                                    startangle=90, 
                                    colors=colors)

    # Adicionar legenda à direita
    ax1.legend(wedges, labels,
            title="Hipóteses",
            loc="center left",
            bbox_to_anchor=(1, 0, 0.5, 1),
            prop={'size': 4})  # Diminuir ainda mais o tamanho da fonte da legenda

    # Ajustar o tamanho da fonte das porcentagens
    plt.setp(autotexts, size=4)

    # Ajustar o layout para incluir a legenda
    plt.tight_layout()

    st.pyplot(fig1)


    # Exibindo tabela de alunos com cores padronizadas
    st.subheader('Tabela de Alunos por Hipótese')
    color_map = {
        'Alfabética': '#86E085',
        'Silábico-alfabética': '#C8FFBB',
        'Silábica c/ valor': '#FFF6A1',
        'Silábica s/ valor': '#FFC9A3',
        'Pré-silábica': '#FFA9B8',
        'Não se aplica': '#FFFFFF'
    }

    def highlight_hypothesis(val):
        color = color_map.get(val, '#FFFFFF')
        return f'background-color: {color}'

    styled_data = data[['student_name', 'hypothesis_name']].style.applymap(highlight_hypothesis, subset=['hypothesis_name'])
    st.dataframe(styled_data, width=1000)

# Função para analisar os dados da turma e fornecer dicas
def analyze_class_data(data, groq_api_key):
    # Gerar o prompt para análise
    prompt = generate_prompt_for_analysis(data)
    # Processar o prompt com a API Groq
    tips = process_with_groq(groq_api_key, prompt)
    return tips

# Função principal para lidar com a lógica do aplicativo
def main():
    configure_ui()
  
    # Carregar os dados do CSV
    try:
        data = pd.read_csv('dados.csv')
        
        # Atualizar o método deprecated para o novo método map
        def highlight_hypothesis(val):
            color = color_map.get(val, '#FFFFFF')
            return f'background-color: {color}'
        
        styled_data = data[['student_name', 'hypothesis_name']].style.map(
            highlight_hypothesis, 
            subset=['hypothesis_name']
        )
        
    except Exception as e:
        st.error(f"Erro ao carregar os dados do CSV: {e}")
        return


    turma, componente, unidade_tematica, objetivo_conhecimento = get_user_inputs(data)

    # Dados simulados para exemplo
    teacher = {'name': 'Silva'}
    school = {'name': 'Escola Futuro Brilhante'}
    class_data = {'name': turma, 'year': '2023'}

    # Exibindo informações da professora, escola e turma no topo da página
    st.markdown(f"### Olá, Professora {teacher['name']}!")
    st.markdown(f"**Escola:** {school['name']}")
    st.markdown(f"**Turma e Ano:** {class_data['name']} - {class_data['year']}")

    current_month = datetime.datetime.now().strftime("%B de %Y")

    # Resumo estratégico dos resultados das hipóteses em porcentagem
    st.subheader("Resumo Estratégico")
    hypothesis_counts = data['hypothesis_name'].value_counts(normalize=True) * 100
    for hypothesis, percentage in hypothesis_counts.items():
        st.write(f"- **{hypothesis}:** {percentage:.1f}%")

    # Análise da IA da Llama
    st.subheader("📊 Análise da IA da Llama")
    try:
        groq_api_key = st.secrets["api"]["groq_api_key"]
        tips = analyze_class_data(data, groq_api_key)
        if tips:
            st.markdown(
                f"""
                <div style="background-color:#f0f8ff; padding:15px; border-radius:10px;">
                <h3 style="color:#2a9d8f;">💡 Dicas da IA:</h3>
                <p style="font-size:16px; color:#264653;">{tips}</p>
                </div>
                """,
                unsafe_allow_html=True
            )
        else:
            st.error("❌ Erro ao processar a análise com a API Groq.")
    except Exception as e:
        st.error(f"Erro ao analisar os dados com a IA da Llama: {e}")

    tabs = st.tabs(["📊 Dados da Classe", "📝 Gerar Atividade"])

    with tabs[0]:
        display_class_data(data, turma)

    with tabs[1]:
        if st.button("Gerar Atividade"):
            try:
                api_token = st.secrets["api"]["api_token"]
                st.info("🚀 Gerando a atividade, por favor, aguarde...")
                try:
                    prompt = generate_prompt_for_activity(componente, unidade_tematica)
                    atividade_texto = generate_activity_with_rag(api_token, prompt)
                    if atividade_texto:
                        st.success("✅ Requisição à API principal bem-sucedida.")
                        resposta_final = process_with_groq(groq_api_key, atividade_texto)

                        if resposta_final:
                            st.markdown(
                                f"""
                                <div style="background-color:#f0f8ff; padding:15px; border-radius:10px;">
                                <h3 style="color:#2a9d8f;">📝 Resultado da Atividade:</h3>
                                <p style="font-size:16px; color:#264653;">{resposta_final}</p>
                                </div>
                                """,
                                unsafe_allow_html=True
                            )
                        else:
                            st.error("❌ Erro ao processar a atividade com a API Groq.")
                    else:
                        st.error("❌ Erro ao fazer a requisição à API principal. Verifique as credenciais e tente novamente.")
                except Exception as e:
                    st.error(f"❌ Erro ao fazer a requisição à API principal: {e}")
            except KeyError as e:
                st.error(f"Erro ao carregar as credenciais da API: {e}")
            except Exception as e:
                st.error(f"Erro ao gerar a atividade: {e}")

if __name__ == "__main__":
    main()
