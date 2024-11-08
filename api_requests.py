import requests
import json
from groq import Groq

def fetch_activity(api_token, tema, nivel_dificuldade):
    """Faz uma requisição à API principal para obter a atividade.

    Parâmetros:
    api_token (str): Token de autenticação da API principal.
    tema (str): Tema da atividade a ser gerada.
    nivel_dificuldade (str): Nível de dificuldade da atividade.

    Retorna:
    str: Texto concatenado dos fragmentos da atividade ou None se a requisição falhar.
    """
    # URL da API principal para obter os fragmentos de texto
    url_fragments = "https://ragne.codebit.dev/rag/text-fragments"

    # Cabeçalho da requisição com autenticação
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_token}"
    }

    # Payload contendo o pedido da atividade
    payload_atividade = {
        "question": f"Crie uma atividade de {tema.lower()} com nível {nivel_dificuldade.lower()} para alunos de ensino fundamental."
    }

    # Envio da requisição POST para a API
    response = requests.post(url_fragments, headers=headers, data=json.dumps(payload_atividade))

    # Verificação do status da resposta
    if response.status_code in [200, 201]:
        # Extrai o conteúdo JSON da resposta e concatena os textos dos fragmentos
        fragmentos = response.json()
        print("Status: Requisição bem-sucedida.")  # Adiciona um status para debug
        return "".join([frag['text'] for frag in fragmentos])
    else:
        print(f"Status: Erro na requisição. Código {response.status_code}")  # Adiciona um status de erro
    # Retorna None em caso de falha na requisição
    return None

def process_with_groq(groq_api_key, prompt):
    """Processa o texto com a API Groq para gerar uma atividade detalhada.

    Parâmetros:
    groq_api_key (str): Chave de API para autenticação com a API Groq.
    prompt (str): Prompt de texto para ser processado pela API.

    Retorna:
    str: Resposta gerada pela API ou None se falhar.
    """
    # Criação do cliente da API Groq com a chave fornecida
    client = Groq(api_key=groq_api_key)

    # Envio da requisição de conclusão de chat para a API Groq
    completion = client.chat.completions.create(
        model="llama3-8b-8192",
        messages=[{
            "role": "user",
            "content": prompt
        }],
        temperature=0.7,
        max_tokens=1500,
        top_p=1,
        stream=True,
        stop=None
    )

    resposta_final = ""
    # Iteração sobre os chunks de resposta recebidos
    for chunk in completion:
        # Verifica se a resposta contém conteúdo válido
        if hasattr(chunk, 'choices') and chunk.choices[0].delta.content:
            resposta_final += chunk.choices[0].delta.content

    # Verifica se a resposta é válida e imprime o status
    if resposta_final:
        print("Status: Resposta processada com sucesso.")  # Status de sucesso
        return resposta_final
    else:
        print("Status: Falha ao processar a resposta.")  # Status de falha
    return None
