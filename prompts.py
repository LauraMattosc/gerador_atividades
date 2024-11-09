# Função que retorna o prompt para a geração de atividades

def get_lesson_sequence_prompt(informacoes_turma):
    """Retorna um prompt formatado para a criação de uma sequência de aulas personalizadas para alfabetização.

    Parâmetros:
    informacoes_turma (str): Informações detalhadas sobre a turma e os objetivos pedagógicos.

    Retorna:
    str: Prompt formatado para ser processado por uma API que gera sequências de aulas.
    """
    print("Status: Gerando o prompt para a criação da sequência de aulas.")  # Mensagem de status para debug

    prompt = f"""
    Aja como se fosse uma professora brasileira experiente dos anos iniciais do ensino fundamental de Língua Portuguesa e elabore uma sequência de 3 aulas para o 2º ano do ensino fundamental. As aulas devem seguir as diretrizes da BNCC e abordar escrita compartilhada e autônoma, mantendo a estética da alfabetização com o uso de exemplos, tabelas ou jogos. A sequência deve considerar uma turma heterogênea, com atividades que possam ser realizadas em pequenos grupos e uma duração máxima de 30 minutos por aula.

    Informações sobre a turma e instruções de planejamento:
    {informacoes_turma}

    Estrutura da sequência de aulas esperada:
    
    **Aula 1:**
    1. **Introdução e Contexto**: Apresentação do tema de forma atrativa para os alunos, relacionando-o aos interesses deles (por exemplo, animais, esportes e aventuras).
    2. **Passo a Passo da Atividade**:
       - **Atividade para nível Pré-silábico e Silábico sem Valor**:
         - Descrição: [Exemplo de atividade com manipulação de sílabas e sons]
         - Tempo: [Defina o tempo estimado para essa etapa]
         - Possíveis Dificuldades: [Dificuldades que os alunos podem encontrar]
       - **Atividade para nível Silábico-Alfabético**:
         - Descrição: [Exemplo de atividade de leitura de frases simples e formação de palavras]
         - Tempo: [Defina o tempo estimado para essa etapa]
         - Possíveis Dificuldades: [Dificuldades que os alunos podem encontrar]
       - **Atividade para nível Alfabético**:
         - Descrição: [Exemplo de exercício de leitura e compreensão de textos curtos]
         - Tempo: [Defina o tempo estimado para essa etapa]
         - Possíveis Dificuldades: [Dificuldades que os alunos podem encontrar]
    3. **Conclusão e Observações para o Professor**: Resuma a aula, enfatizando o progresso esperado e dando dicas para os próximos passos.

    **Aula 2:**
    - [Siga o mesmo formato da Aula 1 com novos conteúdos e atividades adaptadas para cada nível.]

    **Aula 3:**
    - [Siga o mesmo formato da Aula 1 com novos conteúdos e atividades adaptadas para cada nível.]

    **Observações Gerais**:
    - Cada aula deve ser dinâmica, garantindo o engajamento de todos os alunos e estimulando o desenvolvimento de suas habilidades de escrita e leitura de acordo com seu nível.
    - Considere o uso de exemplos e atividades que conectem com os interesses dos alunos.
    - Sugira adaptações para lidar com as dificuldades comuns em cada nível de desenvolvimento.

    """

    print("Status: Prompt gerado com sucesso.")  # Mensagem de status para debug
    return prompt
