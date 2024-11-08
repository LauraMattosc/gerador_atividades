# Função que retorna o prompt para a geração de atividades

def get_activity_prompt(atividade_texto):
    """Retorna um prompt formatado para a API Groq com base no texto da atividade.

    Parâmetros:
    atividade_texto (str): Texto base da atividade gerada pela API principal.

    Retorna:
    str: Prompt formatado pronto para ser processado pela API Groq.
    """
    print("Status: Gerando o prompt para a API Groq.")  # Status para debug

    prompt = f"""
    Baseado nas informações fornecidas a seguir, crie uma atividade, com um passo a passo claro, que possa ser utilizada por um professor do ensino fundamental. A atividade deve incluir:
    - Introdução e contexto da atividade.
    - Descrição detalhada dos passos que os alunos devem seguir.
    - Perguntas desafiadoras que incentivem o pensamento crítico.
    - Explicações claras para ajudar na resolução das questões.
    - Dicas ou observações importantes para o professor.

    Informações fornecidas: {atividade_texto}

    Formato da resposta esperado:
    1. **Introdução**
    2. **Passo 1: [Descrição]**
    - Pergunta: [Exemplo de questão]
    - Dica: [Dica para o professor]
    3. **Passo 2: [Descrição]**
    - Pergunta: [Exemplo de questão]
    - Dica: [Dica para o professor]
    4. **Conclusão e observações finais**
    """

    print("Status: Prompt gerado com sucesso.")  # Status para debug
    return prompt
