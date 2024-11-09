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
    url_fragments = "https://ragne.codebit.dev/rag/text-fragments"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_token}"
    }
    payload_atividade = {
        "question": f"Crie uma atividade de {tema.lower()} com nível {nivel_dificuldade.lower()} para alunos de ensino fundamental."
    }

    try:
        response = requests.post(url_fragments, headers=headers, data=json.dumps(payload_atividade))
        response.raise_for_status()
        fragmentos = response.json()
        return "".join([frag['text'] for frag in fragmentos])
    except requests.exceptions.RequestException as e:
        print(f"Erro na requisição: {e}")
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

    try:
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
            print("Falha ao processar a resposta.")
            return None
    except Exception as e:
        print(f"Erro ao processar com Groq: {e}")
        return None

def generate_activity_with_rag(api_token, tema, nivel_dificuldade):
    """Gera uma atividade usando a API RAG.

    Parâmetros:
    api_token (str): Token de autenticação da API principal.
    tema (str): Tema da atividade a ser gerada.
    nivel_dificuldade (str): Nível de dificuldade da atividade.

    Retorna:
    str: Texto da atividade gerada ou None se a requisição falhar.
    """
    url = "https://api.exemplo.com/rag"
    headers = {"Authorization": f"Bearer {api_token}"}
    data = {"tema": tema, "nivel_dificuldade": nivel_dificuldade}

    try:
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()
        return response.json().get("atividade_texto")
    except requests.exceptions.RequestException as e:
        print(f"Erro na requisição RAG: {e}")
        return None

def generate_activity_with_llama(api_token, tema, nivel_dificuldade):
    """Gera uma atividade usando a API LLaMA.

    Parâmetros:
    api_token (str): Token de autenticação da API principal.
    tema (str): Tema da atividade a ser gerada.
    nivel_dificuldade (str): Nível de dificuldade da atividade.

    Retorna:
    str: Texto da atividade gerada ou None se a requisição falhar.
    """
    url = "https://api.exemplo.com/llama"
    headers = {"Authorization": f"Bearer {api_token}"}
    data = {"tema": tema, "nivel_dificuldade": nivel_dificuldade}

    try:
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()
        return response.json().get("atividade_texto")
    except requests.exceptions.RequestException as e:
        print(f"Erro na requisição LLaMA: {e}")
        return None
