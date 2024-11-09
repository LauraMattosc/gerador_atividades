def generate_prompt_for_activity(componente, unidade_tematica):
    """Retorna um prompt formatado para a criação de uma atividade estruturada."""
    
    prompt = f"""
    Crie uma atividade didática para {componente} focada em {unidade_tematica}.
    
    Estruture a resposta no seguinte formato:
    
    TÍTULO DA ATIVIDADE:
    
    OBJETIVO:
    - Descreva brevemente o que os alunos aprenderão
    
    MATERIAIS:
    - Liste os materiais necessários
    
    PASSO A PASSO:
    1. Primeiro passo
    2. Segundo passo
    3. Terceiro passo
    
    AVALIAÇÃO:
    - Como verificar se os alunos aprenderam
    
    Mantenha a linguagem simples e direta. Atividade para 20 minutos de duração.
    """

    return prompt

