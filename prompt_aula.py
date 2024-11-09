def generate_prompt_for_activity(componente, unidade_tematica):
    """Retorna um prompt formatado para a criação de uma atividade para a aula."""
    
    prompt = f"""
    Aja como se fosse uma professora experiente dos anos iniciais do ensino fundamental, especializada em alfabetização e familiarizada com a BNCC. Elabore um plano de aula de escrita compartilhada e autônoma para uma turma de 2º ano com níveis variados de desenvolvimento de escrita. A aula deve considerar hipóteses de escrita pré-silábica, silábica sem valor sonoro, silábica com valor sonoro, silábica-alfabética e alfabética.
    A aula deve incluir:
    Duração total de 40 minutos e ser dividida em etapas com descrição das atividades, tempo de execução e objetivos de cada uma.
    Possíveis dificuldades de aprendizagem e estratégias para ajudar alunos com diferentes hipóteses de escrita.
    Exemplos práticos e engajadores, como jogos, tabelas ou imagens para estimular o aprendizado.
    A turma tem a seguinte composição:
    Pré-silábico: 5 alunos
    Silábico sem valor sonoro: 8 alunos
    Silábico com valor sonoro: 7 alunos
    Silábico-Alfabética: 3 alunos
    Alfabética: 2 alunos
    Estruture o plano para promover o envolvimento de todos os alunos e apoiar o avanço individual de cada um.
"""

    return prompt

# Exemplo de uso:
print(generate_prompt_for_activity("Língua Portuguesa", "Escrita compartilhada e autônoma"))
