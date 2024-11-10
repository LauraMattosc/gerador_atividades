import json
from groq import Groq

def fetch_activity(api_token, componente, unidade_tematica):
    """Lê os fragmentos de atividade a partir do arquivo fonte.json.

    Parâmetros:
    api_token (str): Token de autenticação da API principal (não mais necessário).
    componente (str): Componente da atividade a ser gerada.
    unidade_tematica (str): Unidade temática da atividade.

    Retorna:
    str: Texto concatenado dos fragmentos da atividade.
    """
    try:
        with open('fonte.json', 'r', encoding='utf-8') as file:
            fragmentos = json.load(file)
            return "".join([frag['text'] for frag in fragmentos if 'text' in frag])
    except FileNotFoundError:
        print("Erro: O arquivo fonte.json não foi encontrado.")
        return None
    except json.JSONDecodeError:
        print("Erro: Falha ao decodificar o arquivo JSON.")
        return None

def process_with_groq(groq_api_key, prompt):
    """Processa o texto com a API Groq para gerar uma atividade detalhada."""
    try:
        client = Groq(api_key=groq_api_key)
        print(" Iniciando processamento com Groq...")
        
        # Verificação do tamanho do prompt
        if len(prompt) > 4000:  # ajuste este limite conforme necessário
            print(" Alerta: Prompt muito longo")
            prompt = prompt[:4000]  # Cortar o prompt se necessário
            print(" Reduzindo prompt para 4000 caracteres...")
        
        completion = client.chat.completions.create(
            model="llama3-8b-8192",
            messages=[{
                "role": "user",
                "content": prompt
            }],
            temperature=1,
            max_tokens=1024,  # reduzido para evitar respostas muito longas
            top_p=1,
            stream=True,
            stop=None
        )
        
        resposta_final = ""
        print(" Recebendo resposta...")
        
        for chunk in completion:
            if hasattr(chunk, 'choices') and chunk.choices[0].delta.content:
                resposta_final += chunk.choices[0].delta.content
        
        if resposta_final:
            print(" Resposta gerada com sucesso!")
            return resposta_final
        else:
            print(" Resposta vazia recebida")
            return None
            
    except Exception as e:
        print(f" Erro específico: {str(e)}")
        print(f" Tipo de erro: {type(e).__name__}")
        return None

# A função generate_activity_with_rag foi removida porque não é mais necessária para essa abordagem.
