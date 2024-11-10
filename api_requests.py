import requests
from typing import Optional, Dict, Any
import json
import os
import streamlit as st
import logging

# Configuração do logger para imprimir logs no terminal
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
            st.success("✅ API key carregada com sucesso")
            logger.info("API key carregada com sucesso.")
            return api_key
        else:
            st.error("❌ API key não encontrada")
            logger.warning("API key não encontrada.")
            return None
    except Exception as e:
        st.error(f"❌ Erro ao carregar API key: {e}")
        logger.error(f"Erro ao carregar API key: {e}")
        return None

def call_api(prompt: str) -> Optional[str]:
    """
    Processa o prompt usando a API Groq e retorna um plano genérico em caso de falha.

    Parâmetros:
    prompt (str): O prompt a ser processado.

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
            "model": "llama2-70b-4096",
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

        st.info("🔄 Enviando requisição para API Groq...")
        logger.info("Enviando requisição para a API Groq com o seguinte payload:")
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
                logger.info(f"Resposta JSON da API: {json.dumps(result, indent=2, ensure_ascii=False)}")
                content = result["choices"][0]["message"]["content"]
                st.success("✅ Resposta da API recebida com sucesso")
                return content
            except (KeyError, IndexError, json.JSONDecodeError) as parse_error:
                st.error("❌ Erro ao processar a estrutura da resposta da API.")
                logger.error(f"Erro ao processar a estrutura da resposta da API: {parse_error}")
                return generate_generic_plan()
        elif response.status_code == 429:
            st.error("❌ Limite de requisições da API foi atingido. Tente novamente mais tarde.")
            logger.error("Limite de requisições da API atingido. Verifique a quota disponível.")
        elif response.status_code == 401:
            st.error("❌ Falha de autenticação. Verifique a chave da API.")
            logger.error("Falha de autenticação. Verifique a chave da API.")
        elif response.status_code == 500:
            st.error("❌ Erro interno do servidor da API. Tente novamente mais tarde.")
            logger.error("Erro interno do servidor da API.")
        else:
            st.error(f"❌ Erro na API: {response.status_code}")
            st.error(f"Detalhes da resposta da API: {response.text}")
            logger.error(f"Erro na API: {response.status_code} - Detalhes: {response.text}")

        return generate_generic_plan()

    except requests.exceptions.Timeout:
        st.error("⏱️ Timeout na requisição à API")
        logger.error("Timeout na requisição à API.")
        return generate_generic_plan()
    except requests.exceptions.RequestException as e:
        st.error(f"❌ Erro na requisição: {e}")
        logger.error(f"Erro na requisição: {e}")
        return generate_generic_plan()
    except Exception as e:
        st.error(f"❌ Erro inesperado: {e}")
        logger.error(f"Erro inesperado: {e}")
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
