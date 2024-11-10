import streamlit as st
from api_requests import call_api

def generate_prompt_for_activity(componente, unidade_tematica, objetivo_de_conhecimento, data="", perfis_turma=""):
    """
    Gera um roteiro de aula detalhado para facilitar o planejamento docente.

    Parâmetros:
    componente (str): O componente curricular.
    unidade_tematica (str): A unidade temática.
    objetivo_de_conhecimento (str): O objetivo de conhecimento.
    data (str, opcional): Data do plano de aula.
    perfis_turma (str, opcional): Perfis da turma.

    Retorna:
    str: Prompt gerado para o planejamento da aula.
    """
    prompt = f"""
    Você é um assistente especializado em planejamento pedagógico. 
    Crie um plano de aula detalhado e personalizado seguindo exatamente esta estrutura:

    # Plano de Aula de {componente} para {unidade_tematica}
    
    ## Informações Gerais 📋
    - **Duração Total:** 40 minutos
    - **Componente Curricular:** {componente}
    - **Unidade Temática:** {unidade_tematica}
    - **Objetivo de Conhecimento:** {objetivo_de_conhecimento}
    - **Data:** {data}

    ## Objetivo Geral 🎯
    [Gere um objetivo específico relacionado ao componente e unidade temática]

    ## Etapas da Aula ⏱️

    ### 1. Abertura e Sensibilização (10 minutos)
    - **Atividade:** [Descreva uma atividade inicial envolvente e contextualizada]
    - **Objetivo:** [Especifique o objetivo desta etapa]
    - **Estratégias por Nível:**
    <div style="background-color:#f0f8ff; padding:15px; border-radius:10px;">
    <h3 style="color:#2a9d8f;">💡 Estratégias Diferenciadas:</h3>
    <ul style="font-size:16px; color:#264653;">
        <li><strong>Pré-silábicos:</strong> [Estratégia específica]</li>
        <li><strong>Silábicos sem valor sonoro:</strong> [Estratégia específica]</li>
        <li><strong>Silábicos com valor sonoro:</strong> [Estratégia específica]</li>
        <li><strong>Silábico-Alfabética e Alfabética:</strong> [Estratégia específica]</li>
    </ul>
    </div>

    ### 2. Desenvolvimento Principal (15 minutos)
    - **Atividade:** [Descreva a atividade principal]
    - **Metodologia:** [Explique como será conduzida]
    - **Estratégias por Nível:**
    <div style="background-color:#f0f8ff; padding:15px; border-radius:10px;">
    <h3 style="color:#2a9d8f;">💡 Abordagens Específicas:</h3>
    <ul style="font-size:16px; color:#264653;">
        <li><strong>Pré-silábicos:</strong> [Estratégia específica]</li>
        <li><strong>Silábicos sem valor sonoro:</strong> [Estratégia específica]</li>
        <li><strong>Silábicos com valor sonoro:</strong> [Estratégia específica]</li>
        <li><strong>Silábico-Alfabética e Alfabética:</strong> [Estratégia específica]</li>
    </ul>
    </div>

    ### 3. Prática Guiada (10 minutos)
    - **Atividade:** [Descreva a atividade prática]
    - **Organização:** [Como os alunos serão organizados]
    - **Intervenções:** [Como o professor deve intervir]

    ### 4. Fechamento e Avaliação (5 minutos)
    - **Atividade:** [Descreva como será o fechamento]
    - **Verificação:** [Como será feita a verificação da aprendizagem]

    ## Materiais Necessários 📚
    - [Liste todos os materiais necessários]
    - [Inclua materiais específicos para cada nível]

    ## Potenciais Dificuldades e Soluções ⚠️
    <div style="background-color:#fff3e6; padding:15px; border-radius:10px;">
    <h3 style="color:#e76f51;">Antecipando Desafios:</h3>
    <ul style="font-size:16px; color:#264653;">
        <li><strong>Dificuldade 1:</strong> [Descreva] → Solução: [Proposta]</li>
        <li><strong>Dificuldade 2:</strong> [Descreva] → Solução: [Proposta]</li>
        <li><strong>Dificuldade 3:</strong> [Descreva] → Solução: [Proposta]</li>
    </ul>
    </div>

    ## Avaliação e Acompanhamento 📊
    - **Critérios:** [Liste os critérios de avaliação]
    - **Registros:** [Como será feito o registro do desenvolvimento]

    Importante:
    1. Adapte todas as atividades ao perfil específico da turma fornecido
    2. Mantenha o formato markdown com os estilos HTML fornecidos
    3. Use emojis apropriados para cada seção
    4. Personalize as estratégias de acordo com os níveis de aprendizagem
    5. Mantenha a formatação visual com as divs estilizadas
    """
    return prompt

def create_lesson_plan(componente, unidade_tematica, objetivo_de_conhecimento, data="", perfis_turma=""):
    """
    Gera e processa o plano de aula usando a API Groq.

    Parâmetros:
    componente (str): O componente curricular.
    unidade_tematica (str): A unidade temática.
    objetivo_de_conhecimento (str): O objetivo de conhecimento.
    data (str, opcional): Data do plano de aula.
    perfis_turma (str, opcional): Perfis da turma.

    Retorna:
    str: O plano de aula gerado.
    """
    prompt = generate_prompt_for_activity(componente, unidade_tematica, objetivo_de_conhecimento, data, perfis_turma)
    return call_api(prompt)
