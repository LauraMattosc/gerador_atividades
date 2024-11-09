import os
import streamlit as st
import pandas as pd
import datetime
import matplotlib.pyplot as plt
from sqlalchemy import create_engine
from api_requests import fetch_activity, process_with_groq, generate_activity_with_rag

# Função para carregar os dados do banco de dados
def load_data():
    user = st.secrets["database"]["DB_USER"]
    password = st.secrets["database"]["DB_PASSWORD"]
    host = st.secrets["database"]["DB_HOST"]
    port = st.secrets["database"]["DB_PORT"]
    database = st.secrets["database"]["DB_NAME"]
    connection_string = f'mysql+pymysql://{user}:{password}@{host}:{port}/{database}'
    engine = create_engine(connection_string)
    
    query = "SELECT * FROM diagnostic_assessment"  # Substitua pela sua consulta SQL
    data = pd.read_sql(query, engine)
    return data

# Configuração da interface do Streamlit
def configure_ui():
    """Configura a interface do usuário usando o Streamlit."""
    st.set_page_config(page_title="Painel da Classe e Gerador de Atividades", layout="wide")
    st.title('📊 Painel da Classe e Gerador de Atividades')
    st.write('Este aplicativo combina a visualização de dados da classe com a geração de atividades práticas e envolventes.')

# Entradas principais do usuário
def get_user_inputs():
    """Captura as entradas de dados do usuário.

    Retorna:
    tuple: Contendo as credenciais da API, tema e nível de dificuldade.
    """
    st.sidebar.header("Configurações da Atividade")
    turma = st.sidebar.selectbox("Escolha a turma:", ["1º ano", "2º ano"])
    componente = st.sidebar.selectbox("Escolha o componente:", ["Matemática", "Língua Portuguesa"])
    unidade_tematica = st.sidebar.selectbox("Escolha a unidade temática:", ["Leitura", "Escrita", "Produção de Texto"])
    objetivo_conhecimento = st.sidebar.text_input("Objetivo de conhecimento:")
    return turma, componente, unidade_tematica, objetivo_conhecimento

# Função para buscar dados e mostrar informações da classe
def display_class_data(data):
    # Dados simulados para exemplo
    teacher = {'name': 'Prof. Silva'}
    school = {'name': 'Escola Futuro Brilhante'}
    class_data = {'name': 'Turma A', 'year': '2023'}

    # Exibindo informações da classe
    st.subheader("Informações da Classe")
    st.write(f"**Professor(a):** {teacher['name']}")
    st.write(f"**Escola:** {school['name']}")
    st.write(f"**Turma e Ano:** {class_data['name']} - {class_data['year']}")

    current_month = datetime.datetime.now().strftime("%B de %Y")
    st.write(f"**Data da Sondagem:** {current_month}")

    # Filtrando alunos alfabetizados
    alphabetizados = data[data['hypothesis_id'] == 1]

    # Exibindo tabela de alunos alfabetizados
    st.subheader('Tabela de Alunos Alfabetizados')
    st.dataframe(alphabetizados)

    # Contagem de alunos alfabetizados por classe
    st.subheader('Número de Alunos Alfabetizados por Classe')
    count_per_class = alphabetizados['class_id'].value_counts().reset_index()
    count_per_class.columns = ['Class ID', 'Number of Literate Students']
    st.bar_chart(count_per_class.set_index('Class ID'))

    # Gráfico de pizza de alunos alfabetizados
    st.subheader("Porcentagem de Alunos Alfabetizados")
    total_students = len(data)
    total_alphabetizados = len(alphabetizados)
    labels = ['Alfabetizados', 'Não Alfabetizados']
    sizes = [total_alphabetizados, total_students - total_alphabetizados]
    colors = ['#ff9999','#66b3ff']
    fig1, ax1 = plt.subplots()
    ax1.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90, colors=colors)
    ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    st.pyplot(fig1)

# Função principal para lidar com a lógica do aplicativo
def main():
    configure_ui()
    turma, componente, unidade_tematica, objetivo_conhecimento = get_user_inputs()

    # Carregar as credenciais do arquivo secrets.toml
    try:
        api_token = st.secrets["api"]["api_token"]
        groq_api_key = st.secrets["api"]["groq_api_key"]
    except Exception as e:
        st.error(f"Erro ao carregar as credenciais: {e}")
        return

    # Verificar se as credenciais foram carregadas corretamente
    if not api_token or not groq_api_key:
        st.error("As credenciais da API não foram carregadas corretamente.")
        return

    # Carregar os dados do banco de dados
    data = load_data()

    tabs = st.tabs(["📊 Dados da Classe", "📝 Gerar Atividade"])

    with tabs[0]:
        display_class_data(data)

    with tabs[1]:
        if st.button("Gerar Atividade"):
            if api_token and groq_api_key:
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
            else:
                st.warning("⚠️ Por favor, insira as credenciais da API para continuar.")

if __name__ == "__main__":
    main()
