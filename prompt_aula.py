def generate_prompt_for_activity(componente, unidade_tematica):
    """Gera um prompt para a criação de uma atividade.

    Parâmetros:
    componente (str): Componente da atividade a ser gerada.
    unidade_tematica (str): Unidade temática da atividade.

    Retorna:
    str: Prompt gerado para a criação da atividade.
    """
    prompt = f"Crie uma atividade de {componente.lower()} na unidade temática de {unidade_tematica.lower()} para alunos de ensino fundamental."
    return prompt
