# api_requests.py

import requests
from typing import Optional
import json
import logging
import streamlit as st

# Configuração do logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def load_api_key() -> Optional[str]:
    """
    Carrega a chave da API do arquivo .streamlit/secrets.toml.

    Retorna:
    Optional[str]: A chave da API se encontrada, caso contrário None.
    """
    try:
        api_key = st.secrets.get("groq_api_key")
        if api_key:
            logger.info("API key carregada com sucesso.")
            return api_key
        else:
            logger.warning("API key não encontrada.")
            return None
    except Exception as e:
        logger.error(f"Erro ao carregar API key: {e}")
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
    try:
        api_key = load_api_key()
        if not api_key:
            logger.error("API key não disponível. Abandonando chamada à API.")
            return generate_generic_plan()

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

        logger.info("Enviando requisição para a API com o seguinte payload:")
        logger.info(json.dumps(data, indent=2, ensure_ascii=False))

        response = requests.post(
            "https://api.groq.com/openai/v1/chat/completions",
            headers=headers,
            json=data,
            timeout=30
        )

        logger.info(f"Status da resposta da API: {response.status_code}")
        logger.info(f"Resposta bruta da API: {response.text}")

        if response.status_code == 200:
            try:
                result = response.json()
                content = result["choices"][0]["message"]["content"]
                return content
            except (KeyError, IndexError, json.JSONDecodeError) as parse_error:
                logger.error(f"Erro ao processar a estrutura da resposta da API: {parse_error}")
                return generate_generic_plan()
        else:
            logger.error(f"Erro na API: {response.status_code} - Detalhes: {response.text}")
            return generate_generic_plan()

    except requests.exceptions.RequestException as e:
        logger.error(f"Erro na requisição: {e}")
        return generate_generic_plan()

def generate_generic_plan() -> str:
    """
    Gera um plano de aula genérico formatado para exibição.

    Retorna:
    str: Um plano de aula genérico formatado.
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
