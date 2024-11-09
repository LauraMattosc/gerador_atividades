import streamlit as st
import pandas as pd
import datetime
import matplotlib.pyplot as plt
from api_requests import fetch_activity, process_with_groq, generate_activity_with_rag, generate_activity_with_llama

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
    st.sidebar.header("Configurações da Atividade")import streamlit as st
import pandas as pd
import datetime
import matplotlib.pyplot as plt
from api_requests import fetch_activity, process_with_groq, generate_activity_with_rag, generate_activity_with_llama

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
    api_token = st.sidebar.text_input("🔑 Insira seu token de autenticação da API principal:", type="password")
    groq_api_key = st.sidebar.text_input("🔐 Insira sua chave API do Groq:", type="password")
    tema = st.sidebar.selectbox("📚 Escolha o tema da atividade:", ["Histórias Curtas", "Completar Palavras", "Sílabas", "Rimas", "Leitura de Palavras"])
    nivel_dificuldade = st.sidebar.selectbox("🎚️ Selecione o nível de dificuldade:", ["Fácil", "Médio", "Difícil"]) 
    return api_token, groq_api_key, tema, nivel_dificuldade

# Função para buscar dados e mostrar informações da classe (mock)
def display_class_data():
    # Dados simulados para exemplo
    teacher = {'name': 'Prof. Silva'}
    school = {'name': 'Escola Futuro Brilhante'}
    class_data = {'name': 'Turma A', 'year': '2023'}
    students = pd.DataFrame({
        'name': ['Alice', 'Bruno', 'Carla', 'Daniel'],
        'hypothesis': ['A', 'B', 'A', 'C'],
        'comment': ['Progresso excelente', None, 'Precisa de mais apoio', 'Esforço consistente']
    })

    # Exibindo informações da classe
    st.subheader("Informações da Classe")
    st.write(f"**Professor(a):** {teacher['name']}")
    st.write(f"**Escola:** {school['name']}")
    st.write(f"**Turma e Ano:** {class_data['name']} - {class_data['year']}")

    current_month = datetime.datetime.now().strftime("%B de %Y")
    st.write(f"**Data da Sondagem:** {current_month}")

    st.subheader("Resumo das Hipóteses")
    grouped_hypotheses = students.groupby('hypothesis').size().reset_index(name='Quantidade de Alunos')
    st.table(grouped_hypotheses)

    # Gráfico de barras das hipóteses
    st.subheader("Distribuição das Hipóteses")
    fig, ax = plt.subplots()
    ax.bar(grouped_hypotheses['hypothesis'], grouped_hypotheses['Quantidade de Alunos'], color='skyblue')
    ax.set_xlabel('Hipótese')
    ax.set_ylabel('Quantidade de Alunos')
    ax.set_title('Distribuição das Hipóteses dos Alunos')
    st.pyplot(fig)

    st.subheader("Lista de Alunos")
    for _, row in students.iterrows():
        st.write(f"**Nome:** {row['name']}")
        st.markdown(
            f"<div style='background-color: #E3E4E5; padding: 5px; border-radius: 5px; display: inline-block;'>{row['hypothesis']}</div>",
            unsafe_allow_html=True
        )
        if row['comment']:
            with st.expander("Ver Comentário"):
                st.write(f"{row['comment']}")

# Função principal para lidar com a lógica do aplicativo
def main():
    configure_ui()
    display_class_data()
    api_token, groq_api_key, tema, nivel_dificuldade = get_user_inputs()

    if st.sidebar.button("Gerar Atividade"):
        if api_token and groq_api_key:
            st.info("🚀 Gerando a atividade, por favor, aguarde...")
            atividade_texto = fetch_activity(api_token, tema, nivel_dificuldade)

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
        else:
            st.warning("⚠️ Por favor, insira as credenciais da API para continuar.")

    if st.sidebar.button("Gerar Atividade com RAG"):
        if api_token and groq_api_key:
            st.info("🚀 Gerando a atividade com RAG, por favor, aguarde...")
            atividade_texto = generate_activity_with_rag(api_token, tema, nivel_dificuldade)

            if atividade_texto:
                st.success("✅ Requisição à API principal bem-sucedida.")
                resposta_final = process_with_groq(groq_api_key, atividade_texto)

                if resposta_final:
                    st.markdown(
                        f"""
                        <div style="background-color:#f0f8ff; padding:15px; border-radius:10px;">
                        <h3 style="color:#2a9d8f;">📝 Resultado da Atividade com RAG:</h3>
                        <p style="font-size:16px; color:#264653;">{resposta_final}</p>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )
                else:
                    st.error("❌ Erro ao processar a atividade com a API Groq.")
            else:
                st.error("❌ Erro ao fazer a requisição à API principal. Verifique as credenciais e tente novamente.")
        else:
            st.warning("⚠️ Por favor, insira as credenciais da API para continuar.")

    if st.sidebar.button("Gerar Atividade com LLaMA"):
        if api_token and groq_api_key:
            st.info("🚀 Gerando a atividade com LLaMA, por favor, aguarde...")
            atividade_texto = generate_activity_with_llama(api_token, tema, nivel_dificuldade)

            if atividade_texto:
                st.success("✅ Requisição à API principal bem-sucedida.")
                resposta_final = process_with_groq(groq_api_key, atividade_texto)

                if resposta_final:
                    st.markdown(
                        f"""
                        <div style="background-color:#f0f8ff; padding:15px; border-radius:10px;">
                        <h3 style="color:#2a9d8f;">📝 Resultado da Atividade com LLaMA:</h3>
                        <p style="font-size:16px; color:#264653;">{resposta_final}</p>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )
                else:
                    st.error("❌ Erro ao processar a atividade com a API Groq.")
            else:
                st.error("❌ Erro ao fazer a requisição à API principal. Verifique as credenciais e tente novamente.")
        else:
            st.warning("⚠️ Por favor, insira as credenciais da API para continuar.")

if __name__ == "__main__":
    main()

    api_token = st.sidebar.text_input("🔑 Insira seu token de autenticação da API principal:", type="password")
    groq_api_key = st.sidebar.text_input("🔐 Insira sua chave API do Groq:", type="password")
    tema = st.sidebar.selectbox("📚 Escolha o tema da atividade:", ["Histórias Curtas", "Completar Palavras", "Sílabas", "Rimas", "Leitura de Palavras"])
    nivel_dificuldade = st.sidebar.selectbox("🎚️ Selecione o nível de dificuldade:", ["Fácil", "Médio", "Difícil"]) 
    return api_token, groq_api_key, tema, nivel_dificuldade

# Função para buscar dados e mostrar informações da classe (mock)
def display_class_data():
    # Dados simulados para exemplo
    teacher = {'name': 'Prof. Silva'}
    school = {'name': 'Escola Futuro Brilhante'}
    class_data = {'name': 'Turma A', 'year': '2023'}
    students = pd.DataFrame({
        'name': ['Alice', 'Bruno', 'Carla', 'Daniel'],
        'hypothesis': ['A', 'B', 'A', 'C'],
        'comment': ['Progresso excelente', None, 'Precisa de mais apoio', 'Esforço consistente']
    })

    # Exibindo informações da classe
    st.subheader("Informações da Classe")
    st.write(f"**Professor(a):** {teacher['name']}")
    st.write(f"**Escola:** {school['name']}")
    st.write(f"**Turma e Ano:** {class_data['name']} - {class_data['year']}")

    current_month = datetime.datetime.now().strftime("%B de %Y")
    st.write(f"**Data da Sondagem:** {current_month}")

    st.subheader("Resumo das Hipóteses")
    grouped_hypotheses = students.groupby('hypothesis').size().reset_index(name='Quantidade de Alunos')
    st.table(grouped_hypotheses)

    # Gráfico de barras das hipóteses
    st.subheader("Distribuição das Hipóteses")
    fig, ax = plt.subplots()
    ax.bar(grouped_hypotheses['hypothesis'], grouped_hypotheses['Quantidade de Alunos'], color='skyblue')
    ax.set_xlabel('Hipótese')
    ax.set_ylabel('Quantidade de Alunos')
    ax.set_title('Distribuição das Hipóteses dos Alunos')
    st.pyplot(fig)

    st.subheader("Lista de Alunos")
    for _, row in students.iterrows():
        st.write(f"**Nome:** {row['name']}")
        st.markdown(
            f"<div style='background-color: #E3E4E5; padding: 5px; border-radius: 5px; display: inline-block;'>{row['hypothesis']}</div>",
            unsafe_allow_html=True
        )
        if row['comment']:
            with st.expander("Ver Comentário"):
                st.write(f"{row['comment']}")

# Função principal para lidar com a lógica do aplicativo
def main():
    configure_ui()
    display_class_data()
    api_token, groq_api_key, tema, nivel_dificuldade = get_user_inputs()

    if st.sidebar.button("Gerar Atividade"):
        if api_token and groq_api_key:
            st.info("🚀 Gerando a atividade, por favor, aguarde...")
            atividade_texto = fetch_activity(api_token, tema, nivel_dificuldade)

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
        else:
            st.warning("⚠️ Por favor, insira as credenciais da API para continuar.")

    if st.sidebar.button("Gerar Atividade com RAG"):
        if api_token and groq_api_key:
            st.info("🚀 Gerando a atividade com RAG, por favor, aguarde...")
            atividade_texto = generate_activity_with_rag(api_token, tema, nivel_dificuldade)

            if atividade_texto:
                st.success("✅ Requisição à API principal bem-sucedida.")
                resposta_final = process_with_groq(groq_api_key, atividade_texto)

                if resposta_final:
                    st.markdown(
                        f"""
                        <div style="background-color:#f0f8ff; padding:15px; border-radius:10px;">
                        <h3 style="color:#2a9d8f;">📝 Resultado da Atividade com RAG:</h3>
                        <p style="font-size:16px; color:#264653;">{resposta_final}</p>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )
                else:
                    st.error("❌ Erro ao processar a atividade com a API Groq.")
            else:
                st.error("❌ Erro ao fazer a requisição à API principal. Verifique as credenciais e tente novamente.")
        else:
            st.warning("⚠️ Por favor, insira as credenciais da API para continuar.")

    if st.sidebar.button("Gerar Atividade com LLaMA"):
        if api_token and groq_api_key:
            st.info("🚀 Gerando a atividade com LLaMA, por favor, aguarde...")
            atividade_texto = generate_activity_with_llama(api_token, tema, nivel_dificuldade)

            if atividade_texto:
                st.success("✅ Requisição à API principal bem-sucedida.")
                resposta_final = process_with_groq(groq_api_key, atividade_texto)

                if resposta_final:
                    st.markdown(
                        f"""
                        <div style="background-color:#f0f8ff; padding:15px; border-radius:10px;">
                        <h3 style="color:#2a9d8f;">📝 Resultado da Atividade com LLaMA:</h3>
                        <p style="font-size:16px; color:#264653;">{resposta_final}</p>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )
                else:
                    st.error("❌ Erro ao processar a atividade com a API Groq.")
            else:
                st.error("❌ Erro ao fazer a requisição à API principal. Verifique as credenciais e tente novamente.")
        else:
            st.warning("⚠️ Por favor, insira as credenciais da API para continuar.")

if __name__ == "__main__":
    main()
