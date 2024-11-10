import anvil.server
from groq import Groq  # Certifique-se de que a biblioteca Groq está instalada e disponível

@anvil.server.http_endpoint("/prompt", methods=["POST"])
def prompt():
    # Extrai o JSON completo do corpo da requisição
    data = anvil.server.request.body_json
    
    # Verifica se o campo 'text' existe no JSON recebido
    prompt = data.get("prompt")
    if prompt is None:
        return {"status": "error", "message": "Parâmetro 'text' não encontrado"}
    
    print(f"Texto recebido: {prompt}")
  # Inicialize o cliente Groq
    client = Groq(api_key=groq_api_key)

    # Crie a chamada de conclusão de chat
    completion = client.chat.completions.create(
        model="llama-3.2-90b-text-preview",
        messages=[{"role": "user", "content": prompt}],
        temperature=1,
        max_tokens=1024,
        top_p=1,
        stream=True,
        stop=None,
    )

    # Concatene a resposta conforme ela é recebida em chunks
    response_text = ""
    for chunk in completion:
        response_text += chunk.choices[0].delta.content or ""

    #return response_text
    return {"status": "success", "received_text": response_text}

# Defina o endpoint GET
@anvil.server.http_endpoint("/hello", methods=["GET"])
def hello(prompt=""):
  # Inicialize o cliente Groq
    client = Groq(api_key=groq_api_key)

    # Crie a chamada de conclusão de chat
    completion = client.chat.completions.create(
        model="llama-3.2-3b-preview",
        messages=[{"role": "user", "content": prompt}],
        temperature=1,
        max_tokens=1024,
        top_p=1,
        stream=True,
        stop=None,
    )

    # Concatene a resposta conforme ela é recebida em chunks
    response_text = ""
    for chunk in completion:
        response_text += chunk.choices[0].delta.content or ""

    return response_text
  #return f"Você enviou o prompt: {prompt}"
