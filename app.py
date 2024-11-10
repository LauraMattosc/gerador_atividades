import streamlit as st
import pandas as pd
import datetime
import matplotlib.pyplot as plt
from api_requests import call_api  # Importando a função da API
from prompt_dicas import generate_prompt_for_analysis
from prompt_aula import generate_prompt_for_activity
import logging
from PIL import Image

# Configuração da interface do Streamlit
st.set_page_config(page_title="Painel da Classe e Gerador de Aulas", layout="wide")

# Configuração do logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Adicionar as imagens
# Exibe o logo do AlfaTutor (imagem maior)
image_logo = Image.open("AlfaTutor.png")

# Exibe a imagem com ajuste automático da largura
st.image(image_logo, use_column_width=True)

# Texto abaixo da imagem
st.write(
    "A sua tutora para apoiar alfabetização para cada criança, em cada sala de aula."
)

# Título principal em grande
st.write("# Olá, professora Patrícia! :wave:")

# Texto menor abaixo
st.write(
    "Sou a AlfaTutor 🦉, sua companhia na jornada da alfabetização! :star2:\n\n"
    "Estou aqui para ajudar você a garantir que todas as suas crianças alcancem o sucesso na leitura e escrita.\n\n"
)

def configure_ui():
    st.write('Vamos ver como está sua turma?')

def get_user_inputs(data):
    """Captura as entradas de dados do usuário."""
    st.sidebar.header("Configurações da Atividade")
    turmas = data['class_name'].unique()
    turma = st.sidebar.selectbox("Escolha a turma:", turmas)
    componente = st.sidebar.selectbox("Escolha o componente:", ["Língua Portuguesa", "Matemática"])
    unidade_tematica = st.sidebar.selectbox("Escolha a unidade temática:", ["Leitura", "Escrita", "Produção de Texto"])
    objetivos_map = {
        "Leitura": ["Compreensão em Leitura"],
        "Escrita": ["Produção de Textos"],
        "Oralidade": ["Contação de Histórias"]
    }
    objetivo_conhecimento = st.sidebar.selectbox("Objetivo de Conhecimento", objetivos_map[unidade_tematica])
    
    return turma, componente, unidade_tematica, objetivo_conhecimento

def display_class_data(data: pd.DataFrame, turma: str, nome_busca: str = ""):
    """Exibe os dados da turma, como gráfico e tabela de hipóteses."""
    data = data[data['class_name'] == turma]
    
    # Início da explicação das hipóteses de escrita
    st.write("### Explicação das Hipóteses de Escrita")
    with st.expander("Clique para ver as explicações", expanded=True):
        # Correção do HTML, garantindo que as tags estejam corretas e a formatação seja limpa
        st.markdown(
            """
            <div style="background-color:#E6F7FF; padding:10px; border-radius:8px; margin-bottom:10px;">
                <h4 style="color:#005A9C; font-size:18px;">Pré-silábica:</h4>
                <p style="font-size:16px; color:#333333;">As produções são marcadas pela não correspondência entre partes do falado e partes do escrito, ou seja, não há correspondência sonora. O uso aleatório de letras, a preferência por algumas delas (como as letras do próprio nome) e elementos gráficos como números e garatujas.</p>
            </div>
            <div style="background-color:#E6F7FF; padding:10px; border-radius:8px; margin-bottom:10px;">
                <h4 style="color:#005A9C; font-size:18px;">Silábico sem valor sonoro:</h4>
                <p style="font-size:16px; color:#333333;">A criança descobre que a quantidade de letras pode se relacionar com a quantidade de sílabas e entende que é preciso variar as letras ao escrever tanto uma palavra quanto um conjunto delas. Nas produções, é comum a utilização de uma letra para cada sílaba. O aluno não usa, necessariamente, letras.</p>
            </div>
            <div style="background-color:#E6F7FF; padding:10px; border-radius:8px; margin-bottom:10px;">
                <h4 style="color:#005A9C; font-size:18px;">Silábico com valor sonoro:</h4>
                <p style="font-size:16px; color:#333333;">A criança entende que cada sílaba é representada por uma vogal ou consoante que expressa seu som correspondente. Em geral, as vogais são usadas para representar cada valor sonoro. Há associação entre a quantidade de letras e quantidade de sílabas (mesmo que não conheçam ainda o conceito de sílaba).</p>
            </div>
            <div style="background-color:#E6F7FF; padding:10px; border-radius:8px; margin-bottom:10px;">
                <h4 style="color:#005A9C; font-size:18px;">Silábico-alfabética:</h4>
                <p style="font-size:16px; color:#333333;">A criança não registra mais só uma letra para cada emissão de som, mas passa a colocar mais letras nos registros silábicos, às vezes usando-as de forma pertinente, às vezes escolhendo-as aleatoriamente. Ao ler o que produziu, é comum que o aluno se incomode com o resultado, pedindo para trocar, eliminar ou acrescentar letras. O incômodo é sinal de que ele está construindo hipóteses mais sofisticadas, aproximando sua escrita da convencional.</p>
            </div>
            <div style="background-color:#E6F7FF; padding:10px; border-radius:8px; margin-bottom:10px;">
                <h4 style="color:#005A9C; font-size:18px;">Alfabética:</h4>
                <p style="font-size:16px; color:#333333;">Produzir registros que podem ser lidos por outras pessoas e começa a se questionar sobre como grafar corretamente as palavras. É nessa fase, em geral, que aparecem dúvidas sobre se a palavra é escrita com x ou ch, por exemplo. O aluno já entendeu que a escrita não é apenas uma transcrição do oral, e que várias letras podem ser usadas para sinalizar um mesmo som, mas há regras e convenções que ditam as adequadas, caso a caso.</p>
            </div>
            """,
            unsafe_allow_html=True
        )
    
    # Agora, exibe o gráfico de pizza
    st.subheader("Veja a distribuição dos seus alunos por hipótese")

    # Contagem e exibição dos gráficos
    hypothesis_counts = data['hypothesis_name'].value_counts(normalize=True) * 100
    labels = hypothesis_counts.index
    sizes = hypothesis_counts.values
    color_map = {
        'Alfabética': '#86E085',
        'Silábico-alfabética': '#C8FFBB',
        'Silábica c/ valor': '#FFF6A1',
        'Silábica s/ valor': '#FFC9A3',
        'Pré-silábica': '#FFA9B8'
    }
    colors = [color_map.get(label, '#FFFFFF') for label in labels]

    # Gráfico de pizza
    fig1, ax1 = plt.subplots(figsize=(3, 2))
    wedges, texts, autotexts = ax1.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=70, colors=colors)

    # Ajusta o tamanho dos rótulos (labels)
    plt.setp(texts, size=4)  # Diminui o tamanho dos rótulos
    plt.setp(autotexts, size=3)  # Diminui o tamanho dos percentuais

    st.pyplot(fig1)

    # Campo de busca por nome logo abaixo do gráfico
    nome_busca = st.text_input("Buscar por nome do aluno:", key=f"nome_busca_{turma}")
    if nome_busca:
        data = data[data['student_name'].str.contains(nome_busca, case=False, na=False)]

    st.subheader('Veja as informações de cada um dos seus alunos')

    # Formatação da tabela com cores
    def highlight_hypothesis(val):
        color = color_map.get(val, "#FFFFFF")
        return f'background-color: {color}'

    styled_data = data.style.apply(
        lambda x: [highlight_hypothesis(v) for v in x], subset=['hypothesis_name']
    )
    st.dataframe(styled_data, width=1500)

def clean_response(response: str) -> str:
    """
    Limpa a resposta da API removendo quebras de linha e múltiplos espaços.
    """
    cleaned_response = response.replace('\n', ' ').replace('\r', '').strip()
    cleaned_response = ' '.join(cleaned_response.split())
    return cleaned_response

def format_tips_as_html(tips: str) -> str:
    """
    Formata as dicas como uma lista ordenada (HTML), onde cada dica é um item numerado.
    
    Parâmetros:
    tips (str): Dicas em formato de string. Cada dica pode ser separada por uma quebra de linha.
    
    Retorna:
    str: Dicas formatadas como lista HTML.
    """
    # Divida as dicas por linha e remova linhas vazias ou espaços extras
    dicas = [dica.strip() for dica in tips.split("\n") if dica.strip()]
    
    # Inicia a lista HTML
    formatted_tips = "<ol>"  # Usando <ol> para uma lista numerada
    
    # Adiciona cada dica como um item de lista <li>
    for dica in dicas:
        formatted_tips += f"<li>{dica}</li>"
    
    # Fecha a lista HTML
    formatted_tips += "</ol>"
    
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
    formatted_plan = formatted_plan.replace("## ", "\n\n## ").replace("### ", "\n\n## ")
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

    st.subheader("Resumo do Nível de Alfabetização da Turma 📊")

    # Count the number of students and percentages
    hypothesis_counts = data['hypothesis_name'].value_counts()
    total_students = hypothesis_counts.sum()
    hypothesis_percentages = (hypothesis_counts / total_students) * 100

    # Display each hypothesis with the number of students and percentage
    for hypothesis, count in hypothesis_counts.items():
        percentage = hypothesis_percentages[hypothesis]
        st.write(f"- **{hypothesis}:** {count} alunos ({percentage:.1f}%)")

    try:
        tips = analyze_class_data(data)
        if tips:
            st.markdown(
                f"""
                <div style="background-color:#f0f8ff; padding:15px; border-radius:10px;">
                <h3 style="color:#2a9d8f;">💡 Dicas da IA 🦙:</h3>
                {tips}
                </div>
                """,
                unsafe_allow_html=True
            )
        else:
            st.warning("Nenhuma dica foi retornada pela API.")
    except Exception as e:
        st.error(f"Erro ao analisar os dados com a IA: {e}")
        logger.error(f"Erro ao analisar os dados com a IA: {e}")

    tab_dados, tab_atividade = st.tabs(["📊 Detalhamento da Turma", "📝 Gerar Aula"])

    with tab_dados:
               # Chama a função para exibir os dados da turma com a busca por nome incluída
        display_class_data(data, turma)

    with tab_atividade:
        st.subheader("Agora vamos preparar a sua próxima aula! 📝")
        
        # Botão para gerar a aula
        if st.button("Gerar Aula"):
            try:
                current_month = datetime.datetime.now().strftime("%B de %Y")  # Obtém o mês atual
                perfis_turma = "Perfil detalhado da turma aqui."  # Substitua com informações reais da turma
                plano_aula = generate_lesson_plan(componente, unidade_tematica, objetivo_conhecimento, current_month, perfis_turma)
                
                # Verifica se o plano de aula foi gerado
                if plano_aula:
                    st.markdown(
                        f"""
                        <div style="background-color:#f9f9f9; padding:20px; border-radius:10px; border:1px solid #e0e0e0; margin-top:20px;">
                            <h3 style="color:#2a9d8f; font-size:24px;">Plano de Aula Gerado! </h3>
                            <p style="font-size:16px; color:#333333;">Aqui está o plano de aula detalhado para a sua turma:</p>
                            <div style="font-size:16px; color:#333333;">
                                {plano_aula}  <!-- Aqui é onde o conteúdo do plano de aula gerado será exibido -->
                            </div>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )
                    
                    # Opções de ação com botões
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        if st.button("📥 Baixar PDF"):
                            st.info("Funcionalidade de download em desenvolvimento.")
                    with col2:
                        if st.button("✏️ Editar Plano"):
                            st.info("Funcionalidade de edição em desenvolvimento.")
                    with col3:
                        if st.button("💾 Salvar"):
                            st.info("Funcionalidade de salvamento em desenvolvimento.")
                else:
                    st.error("❌ Não foi possível gerar o plano de aula. Tente novamente.")
                    
            except Exception as e:
                st.error(f"Erro ao gerar o plano de aula: {e}")


if __name__ == "__main__":
    main()
