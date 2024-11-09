import requests
import json
from groq import Groq

def fetch_activity(api_token, componente, unidade_tematica):
    """Faz uma requisição à API principal para obter a atividade.

    Parâmetros:
    api_token (str): Token de autenticação da API principal.
    componente (str): Componente da atividade a ser gerada.
    unidade_tematica (str): Unidade temática da atividade.

    Retorna:
    str: Texto concatenado dos fragmentos da atividade ou None se a requisição falhar.
    """
    url_fragments = "https://ragne.codebit.dev/rag/text-fragments"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_token}"
    }
    payload_atividade = {
        "question": f"Crie uma atividade de {componente.lower()} na unidade temática de {unidade_tematica.lower()} para alunos de ensino fundamental."
    }
    response = requests.post(url_fragments, headers=headers, data=json.dumps(payload_atividade))
    if response.status_code in [200, 201]:
        fragmentos = response.json()
        return "".join([frag['text'] for frag in fragmentos])
    else:
        print(f"Status: Erro na requisição. Código {response.status_code}")
    return None

def process_with_groq(groq_api_key, prompt):
    """Processa o texto com a API Groq para gerar uma atividade detalhada.

    Parâmetros:
    groq_api_key (str): Chave de API para autenticação com a API Groq.
    prompt (str): Prompt de texto para ser processado pela API.

    Retorna:
    str: Resposta gerada pela API ou None se falhar.
    """
    client = Groq(api_key=groq_api_key)
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
    for chunk in completion:
        if hasattr(chunk, 'choices') and chunk.choices[0].delta.content:
            resposta_final += chunk.choices[0].delta.content
    if resposta_final:
        return resposta_final
    else:
        print("Status: Falha ao processar a resposta.")
    return None

def generate_activity_with_rag(api_token, prompt):
    """Gera uma atividade usando a API RAG.

    Parâmetros:
    api_token (str): Token de autenticação da API principal.
    prompt (str): Prompt gerado para a criação da atividade.

    Retorna:
    str: Texto da atividade gerada ou None se a requisição falhar.
    """
    url = "https://ragne.codebit.dev/rag/text-fragments"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_token}"
    }
    data = {
        "question": prompt
    }

    try:
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()
        resposta_json = response.json()
        if isinstance(resposta_json, list):
            return "".join([frag['text'] for frag in resposta_json])
        else:
            raise Exception(f"Resposta inesperada da API: esperava uma lista, mas recebeu {type(resposta_json)}")
    except requests.exceptions.HTTPError as http_err:
        error_message = response.json().get('message', 'No additional error message provided')
        raise Exception(f"HTTP error occurred: {http_err} - {error_message}")
    except requests.exceptions.ConnectionError as conn_err:
        raise Exception(f"Connection error occurred: {conn_err}")
    except requests.exceptions.Timeout as timeout_err:
        raise Exception(f"Timeout error occurred: {timeout_err}")
    except requests.exceptions.RequestException as req_err:
        raise Exception(f"An error occurred: {req_err}")
