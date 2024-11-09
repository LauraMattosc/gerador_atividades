def generate_prompt_for_analysis(data):
    """Gera um prompt para análise estratégica e objetiva dos alunos da turma.

    Parâmetros:
    data (DataFrame): Dados da turma.

    Retorna:
    str: Prompt gerado a partir dos dados da turma.
    """
    prompt = f"Analise os seguintes dados da turma e forneça dicas curtas,  em português, no máximo 3, elas devem ser sobre a turma selecionada:\n\n{data.to_string()}"
    return prompt
