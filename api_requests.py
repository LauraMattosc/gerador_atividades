from groq import Groq  # Certifique-se de ter instalado a biblioteca correta
import logging
import streamlit as st
from typing import Optional

# Configuração do logger
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

def load_api_key() -> Optional[str]:
    """Carrega a chave da API do arquivo .streamlit/secrets.toml."""
    try:
        logger.debug("Tentando acessar a API key diretamente do secrets.toml...")
        api_key = st.secrets["groq_api_key"]
        if api_key:
            logger.info("API key carregada com sucesso.")
            return api_key
        else:
            logger.warning("API key não encontrada.")
            return None
    except KeyError as e:
        logger.error(f"Chave 'groq_api_key' não encontrada: {e}")
        return None
    except Exception as e:
        logger.error(f"Erro ao carregar API key: {e}")
        return None

def call_api(prompt: str, model: str = "llama3-8b-8192") -> Optional[str]:
    """
    Processa o prompt usando a API Groq e retorna uma resposta ou um plano genérico em caso de falha.
    """
    logger.debug(f"Iniciando chamada à função call_api com o modelo: {model}")
    try:
        api_key = load_api_key()
        if not api_key:
            logger.error("API key não disponível. Abandonando chamada à API.")
            return generate_generic_plan()

        # Inicialize o cliente Groq com a chave da API
        client = Groq(api_key=api_key)

        logger.info("Enviando requisição para a API Groq...")
        completion = client.chat.completions.create(
            model=model,
            messages=[
                {
                    "role": "system",
                    "content": "Você é um especialista em educação, focado em criar planos de aula detalhados e personalizados."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.7,
            max_tokens=4096,
            top_p=1,
            stream=True,  # Streaming de respostas
            stop=None
        )

        logger.debug("Recebendo resposta da API com streaming.")
        
        # Armazena todo o conteúdo da resposta
        response_content = ""
        for chunk in completion:
            part = chunk.choices[0].delta.content or ""
            response_content += part  # Concatena a resposta sem exibir no loop

        # Exibe o conteúdo final limpo uma única vez
        if response_content.strip():
            cleaned_response = clean_response(response_content)
            logger.info("Resposta da API processada com sucesso.")
            return cleaned_response
        else:
            logger.error("❌ O retorno da API foi nulo ou vazio.")
            return generate_generic_plan()

    except Exception as e:
        logger.error(f"Erro ao fazer a chamada à API Groq: {e}")
        return generate_generic_plan()

def clean_response(response: str) -> str:
    """
    Limpa a resposta da API removendo quebras de linha e múltiplos espaços.
    """
    cleaned_response = response.replace('\n', ' ').replace('\r', '').strip()
    cleaned_response = ' '.join(cleaned_response.split())
    return cleaned_response

def generate_generic_plan() -> str:
    """
    Gera um plano de aula genérico formatado para exibição.
    """
    logger.warning("Retornando plano de aula genérico devido a erro.")
    return """
    # Plano de Aula Genérico

    ## Informações Gerais 📋
    - **Duração Total:** 40 minutos
    - **Componente Curricular:** [Componente]
    - **Unidade Temática:** [Unidade Temática]
    - **Objetivo de Conhecimento:** [Objetivo de Conhecimento]

    ## Objetivo Geral 🎯
    Fornecer uma introdução geral ao tema abordado.

    ## Etapas da Aula ⏱️
    ### 1. Abertura e Sensibilização (10 minutos)
    - **Atividade:** Introdução ao tema com discussão breve.
    - **Objetivo:** Engajar os alunos no assunto.

    ### 2. Desenvolvimento Principal (20 minutos)
    - **Atividade:** Explicação detalhada e prática guiada.
    - **Objetivo:** Promover a compreensão e participação ativa dos alunos.

    ### 3. Fechamento e Avaliação (10 minutos)
    - **Atividade:** Revisão e perguntas finais.
    - **Objetivo:** Consolidar o aprendizado e avaliar a compreensão.

    ## Materiais Necessários 📚
    - Material didático básico
    - Quadro branco e marcadores

    ## Avaliação e Acompanhamento 📊
    - Observação direta e registro do progresso dos alunos.
    """

# Código para exibição no Streamlit, garantindo que a resposta seja exibida apenas uma vez:
def display_response(response: Optional[str]):
    if response:
        st.markdown(f"<p>{response}</p>", unsafe_allow_html=True)
