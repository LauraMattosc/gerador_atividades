import streamlit as st
import pandas as pd
import datetime
import matplotlib.pyplot as plt

# Configuração da interface do Streamlit
st.set_page_config(page_title="Painel da Classe e Gerador de Atividades", layout="wide")

def configure_ui():
    """Configura a interface do usuário usando o Streamlit."""
    st.title('📊 Painel da Classe e Gerador de Atividades')
    st.write('Este aplicativo combina a visualização de dados da classe com a geração de atividades práticas e envolventes.')

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
    colors = ['#ff9999', '#ffcc99', '#99ff99']  # Cores específicas para cada hipótese
    fig1, ax1 = plt.subplots(figsize=(6, 4))  # Ajuste o tamanho do gráfico de pizza
    ax1.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90, colors=colors)
    ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    st.pyplot(fig1)

    # Exibindo tabela de alunos alfabetizados
    st.subheader('Tabela de Alunos Alfabetizados')
    styled_data = data[['student_name', 'class_name', 'hypothesis_name']].style.applymap(
        lambda x: 'background-color: #ff9999' if x == 'Hipótese Inicial' else 'background-color: #ffcc99' if x == 'Hipótese Intermediária' else 'background-color: #99ff99',
        subset=['hypothesis_name']
    )
    st.dataframe(styled_data, width=1000)  # Aumenta a largura da tabela

# Função para analisar os dados da turma e fornecer dicas
def analyze_class_data(data):
    # Simulação de análise da IA da Llama
    tips = [
        "📈 **Dica 1:** Concentre-se em atividades de leitura para alunos na Hipótese Inicial.",
        "📝 **Dica 2:** Incentive a escrita criativa para alunos na Hipótese Intermediária.",
        "📚 **Dica 3:** Desafie os alunos na Hipótese Avançada com textos mais complexos."
    ]
    return tips

# Função principal para lidar com a lógica do aplicativo
def main():
    configure_ui()

    # Carregar os dados do CSV
    try:
        data = pd.read_csv('dados.csv')
        st.write("Dados carregados com sucesso.")
    except Exception as e:
        st.error(f"Erro ao carregar os dados do CSV: {e}")
        return

    turma, componente, unidade_tematica, objetivo_conhecimento = get_user_inputs(data)

    # Dados simulados para exemplo
    teacher = {'name': 'Prof. Silva'}
    school = {'name': 'Escola Futuro Brilhante'}
    class_data = {'name': turma, 'year': '2023'}

    # Exibindo informações da professora, escola e turma no topo da página
    st.markdown(f"### Olá, Professora {teacher['name']}!")
    st.markdown(f"**Escola:** {school['name']}")
    st.markdown(f"**Turma e Ano:** {class_data['name']} - {class_data['year']}")

    current_month = datetime.datetime.now().strftime("%B de %Y")
    st.write(f"**Data da Sondagem:** {current_month}")

    # Resumo estratégico dos resultados das hipóteses em porcentagem
    st.subheader("Resumo Estratégico")
    hypothesis_counts = data['hypothesis_name'].value_counts(normalize=True) * 100
    for hypothesis, percentage in hypothesis_counts.items():
        st.write(f"- **{hypothesis}:** {percentage:.1f}%")

    # Análise da IA da Llama
    st.subheader("📊 Análise da IA da Llama")
    tips = analyze_class_data(data)
    for tip in tips:
        st.write(tip)

    tabs = st.tabs(["📊 Dados da Classe", "📝 Gerar Atividade"])

    with tabs[0]:
        display_class_data(data, turma)

    with tabs[1]:
        if st.button("Gerar Atividade"):
            try:
                api_token = st.secrets["api"]["api_token"]
                groq_api_key = st.secrets["api"]["groq_api_key"]
                st.info("🚀 Gerando a atividade, por favor, aguarde...")
                try:
                    # Ajuste a chamada para a função generate_activity_with_rag
                    atividade_texto = generate_activity_with_rag(api_token, componente, unidade_tematica)
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
