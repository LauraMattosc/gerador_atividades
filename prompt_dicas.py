import streamlit as st
from api_requests import call_api

def generate_prompt_for_analysis(data):
    """
    Gera um prompt detalhado para análise estratégica e objetiva dos alunos da turma.
    
    Parâmetros:
    data (DataFrame): Dados da turma.
    
    Retorna:
    str: Prompt gerado a partir dos dados da turma.
    """
    prompt = (
        "Você é um especialista em análise de dados educacionais. Analise os dados da turma abaixo e forneça uma análise com as seguintes características:\n"
        "- Gere três dicas super curtas e objetivas sobre a turma, numeradas de forma clara em português.\n"
        "- Cada dica deve ser focada em informações úteis para o professor, abordando padrões gerais e recomendações práticas.\n"
        "- **Pule uma linha entre cada dica numerada** para melhorar a legibilidade e apresentação. Ou seja, cada dica deve estar em um parágrafo separado.\n"
        "- Use uma linguagem direta e concisa. As dicas devem ser fáceis de entender e implementar.\n"
        "- Destaque um ou dois alunos que se destaquem como outliers, incluindo uma breve descrição do que torna o aluno distinto (por exemplo, um aluno com uma evolução mais rápida, dificuldades em uma área específica, ou características que exigem atenção especial).\n"
        "- Utilize a seguinte estrutura de saída para as dicas numeradas, com uma linha em branco entre elas:\n"
        "  1. [Dica 1: Explicação objetiva e clara]\n"
        "  \n"  # Pulo de linha explícito após a primeira dica
        "  2. [Dica 2: Explicação objetiva e clara]\n"
        "  \n"  # Pulo de linha explícito após a segunda dica
        "  3. [Dica 3: Explicação objetiva e clara]\n"
        "  \n"  # Pulo de linha explícito após a terceira dica
        "- No caso de observar um aluno distinto, forneça o nome e a razão pela qual ele se destaca, por exemplo: '[Aluno X] está apresentando uma evolução mais rápida que os outros, sugerindo uma abordagem pedagógica mais avançada para ele.'\n"
        "- Evite explicações longas ou detalhadas demais. Cada dica deve ser um insight rápido para o professor aplicar na sala de aula.\n\n"
        "Agora, analise os dados da turma abaixo e siga o formato de saída indicado. Apresente as dicas numeradas conforme o exemplo acima.\n\n"
        f"{data.to_string(index=False)}"  # Exibe os dados da turma sem o índice
    )
    return prompt

def analyze_data(data):
    st.write("Gerando análise dos dados da turma...")
    prompt = generate_prompt_for_analysis(data)
    response = call_api(prompt)
    return response