def generate_prompt_for_activity(componente, unidade_tematica, objetivo_de_conhecimento="Desenvolver habilidades de escrita", data=""):
    """Gere um roteiro de aula detalhado para facilitar o planejamento docente."""
    
    prompt = f""" 
    # Plano de Aula de Escrita Compartilhada e Autônoma para o 2º Ano
    
    ## Informações Gerais
    - **Duração Total:** 40 minutos
    - **Componente Curricular:** {componente}
    - **Unidade Temática:** {unidade_tematica}
    - **Objetivo de Conhecimento:** {objetivo_de_conhecimento}
    - **Data:** {data}

    ## Objetivo Geral
    Desenvolver habilidades de escrita considerando as diferentes hipóteses de escrita dos alunos, promovendo a participação ativa e engajamento.

    ## Perfil da Turma
    - **Pré-silábico:** 5 alunos
    - **Silábico sem valor sonoro:** 8 alunos
    - **Silábico com valor sonoro:** 7 alunos
    - **Silábico-Alfabética:** 3 alunos
    - **Alfabética:** 2 alunos

    ## Etapas da Aula

    ### 1. Abertura e Sensibilização (10 minutos)
    - **Atividade:** Roda de conversa com uma imagem ilustrativa (ex.: parque com crianças brincando).
    - **Objetivo:** Ativar o conhecimento prévio e incentivar a oralidade.

    ### 2. Escrita Compartilhada (15 minutos)
    - **Atividade:** Construção de uma frase coletiva no quadro com participação dos alunos.
    - **Exemplo de Frase:** “No parque, as crianças estão brincando.”
    - **Estratégias por Nível:**
        - **Pré-silábicos:** Identificar a primeira letra ou desenhar.
        - **Silábicos sem valor sonoro:** Escrever sons isolados.
        - **Silábicos com valor sonoro:** Identificar mais sons.
        - **Silábico-Alfabética e Alfabética:** Completar ou escrever palavras.

    ### 3. Escrita Autônoma (15 minutos)
    - **Atividade:** Escrever uma frase ou palavras individualmente em fichas.
    - **Estratégias:**
        - **Pré-silábicos:** Alfabeto móvel.
        - **Silábicos:** Tabelas de sílabas.
        - **Alfabéticos:** Revisão e expansão da frase.

    ### 4. Partilha e Fechamento (5 minutos)
    - **Atividade:** Leitura das produções dos alunos.
    - **Objetivo:** Validar a produção e promover a autoestima.

    ## Potenciais Dificuldades e Soluções
    - **Pré-silábicos:** Materiais concretos e visuais.
    - **Silábicos:** Associação som-letra.
    - **Alfabéticos:** Uso de dicionários ilustrados.

    ## Materiais Necessários
    - Imagem ilustrativa, lousa, fichas, lápis, alfabeto móvel, tabelas de sílabas.
    
    """
    
    return prompt
