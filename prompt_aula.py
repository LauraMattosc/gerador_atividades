def generate_prompt_for_activity(componente, unidade_tematica):
    """Retorna um prompt formatado para a criação de uma sequência de aulas personalizadas para alfabetização."""
    
    prompt = f"""
    Plano de aula: {componente}, 2º ano, {unidade_tematica}, 30 minutos.

    1. Objetivo
    2. Materiais
    3. Etapas
    4. Avaliação
    """

    return prompt
