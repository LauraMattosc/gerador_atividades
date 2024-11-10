import requests
from typing import Optional
import json
import logging
import streamlit as st

# Configuração do logger
logging.basicConfig(level=logging.DEBUG)  # Alterado para DEBUG para mais detalhes
logger = logging.getLogger(__name__)

def load_api_key() -> Optional[str]:
    """
    Carrega a chave da API do arquivo .streamlit/secrets.toml.
    
    Retorna:
    Optional[str]: A chave da API se encontrada, caso contrário None.
    """
    try:
        logger.debug("Tentando acessar a API key diretamente do secrets.toml...")
        api_key = st.secrets["groq_api_key"]  # Acessa diretamente a chave
        if api_key:
            logger.info("API key carregada com sucesso.")
            st.write("Debug: API key carregada com sucesso (api_requests).")  # Apenas para verificação
            return api_key
        else:
            logger.warning("API key não encontrada no secrets.toml.")
            st.write("Debug: API key não encontrada no secrets.toml (api_requests).")  # Apenas para verificação
            return None
    except KeyError as e:
        logger.error(f"Chave 'groq_api_key' não encontrada: {e}")
        st.write(f"Debug: Chave 'groq_api_key' não encontrada: {e} (api_requests)")  # Apenas para verificação
        return None
    except Exception as e:
        logger.error(f"Erro ao carregar API key: {e}")
        st.write(f"Debug: Erro ao carregar API key: {e} (api_requests)")  # Apenas para verificação
        return None


def call_api(prompt: str, model: str = "llama2-70b-4096") -> Optional[str]:
    """
    Processa o prompt usando a API e retorna uma resposta ou um plano genérico em caso de falha.

    Parâmetros:
    prompt (str): O prompt a ser processado.
    model (str): O modelo a ser usado na chamada da API.

    Retorna:
    Optional[str]: A resposta da API ou um plano genérico em caso de falha.
    """
    logger.debug("Iniciando chamada à função call_api.")
    try:
        api_key = load_api_key()
        if not api_key:
            logger.error("API key não disponível. Abandonando chamada à API.")
            st.write("Debug: API key não disponível, chamada à API abandonada.")  # Apenas para verificação
            return generate_generic_plan()

        logger.debug("Configurando cabeçalhos da requisição.")
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }

        data = {
            "model": model,
            "messages": [
                {
                    "role": "system",
                    "content": "Você é um especialista em educação, focado em criar planos de aula detalhados e personalizados."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            "temperature": 0.7,
            "max_tokens": 4096
        }

        logger.info("Enviando requisição para a API...")
        logger.debug(f"Payload da requisição: {json.dumps(data, indent=2, ensure_ascii=False)}")

        response = requests.post(
            "https://api.groq.com/openai/v1/chat/completions",
            headers=headers,
            json=data,
            timeout=30
        )

        logger.debug("Recebendo resposta da API.")
        logger.info(f"Status da resposta da API: {response.status_code}")
        logger.debug(f"Resposta da API: {response.text}")

        if response.status_code == 200:
            try:
                result = response.json()
                content = result["choices"][0]["message"]["content"]
                logger.info("Resposta da API processada com sucesso.")
                return content
            except (KeyError, IndexError, json.JSONDecodeError) as parse_error:
                logger.error(f"Erro ao processar a estrutura da resposta da API: {parse_error}")
                st.write(f"Debug: Erro ao processar a resposta da API: {parse_error}")  # Apenas para verificação
                return generate_generic_plan()
        else:
            logger.error(f"Erro na API: {response.status_code} - Detalhes: {response.text}")
            st.write(f"Debug: Erro na API, código {response.status_code}")  # Apenas para verificação
            return generate_generic_plan()

    except requests.exceptions.RequestException as e:
        logger.error(f"Erro na requisição à API: {e}")
        st.write(f"Debug: Erro na requisição à API: {e}")  # Apenas para verificação
        return generate_generic_plan()

def generate_generic_plan() -> str:
    """
    Gera um plano de aula genérico formatado para exibição.

    Retorna:
    str: Um plano de aula genérico formatado.
    """
    logger.warning("Retornando plano de aula genérico devido a erro.")
    st.write("Debug: Retornando plano genérico.")  # Apenas para verificação
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


def fetch_activity(componente: str, unidade_tematica: str, objetivo_conhecimento: str) -> Optional[str]:
    """
    Gera um prompt com base nos parâmetros fornecidos para processar a atividade.

    Parâmetros:
    componente (str): O componente curricular.
    unidade_tematica (str): A unidade temática.
    objetivo_conhecimento (str): O objetivo de conhecimento.

    Retorna:
    Optional[str]: O prompt gerado ou None em caso de falha.
    """
    try:
        prompt = f"""
        # Plano de Aula Personalizado

        ## Informações Básicas
        - Componente: {componente}
        - Unidade Temática: {unidade_tematica}
        - Objetivo de Conhecimento: {objetivo_conhecimento}

        Crie um plano de aula detalhado com as seguintes seções:
        1. Duração total e por atividade
        2. Objetivo geral e específicos
        3. Desenvolvimento da aula (início, meio e fim)
        4. Estratégias diferenciadas por nível
        5. Materiais necessários
        6. Avaliação e acompanhamento
        """
        st.success("✅ Prompt gerado com sucesso")
        logger.info(f"Prompt gerado com sucesso: {prompt}")
        return prompt
    except Exception as e:
        st.error(f"❌ Erro ao gerar prompt: {e}")
        logger.error(f"Erro ao gerar prompt: {e}")
        return None
