import streamlit as st
from groq import Groq
import requests
import json

# Configuração do Streamlit
st.title('🧮 Gerador de Atividades de Matemática Personalizadas')
st.write('Este aplicativo cria atividades de matemática práticas e envolventes para ajudar alunos com dificuldades.')

# Entrada de credenciais
api_token = st.text_input("🔑 Insira seu token de autenticação da API principal:", type="password")
groq_api_key = st.text_input("🔐 Insira sua chave API do Groq:", type="password")

# Seleção de tema e dificuldade
tema = st.selectbox("📚 Selecione o tema da atividade:", ["Frações", "Multiplicação", "Divisão", "Problemas de Palavra"])
nivel_dificuldade = st.selectbox("🎚️ Selecione o nível de dificuldade:", ["Fácil", "Médio", "Difícil"]) 

# Botão para iniciar a geração da atividade
if st.button("Gerar Atividade"):
    # Verificação de preenchimento das credenciais
    if api_token and groq_api_key:
        # URL da API principal
        url_fragments = "https://ragne.codebit.dev/rag/text-fragments"
        
        # Configuração do cabeçalho da requisição
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_token}"
        }
        
        # Payload para requisição
        payload_atividade = {
            "question": f"Crie uma atividade de {tema.lower()} com nível {nivel_dificuldade.lower()} para alunos de ensino fundamental."
        }

        # Requisição à API principal
        st.info("🚀 Gerando a atividade, por favor, aguarde...")
        response = requests.post(url_fragments, headers=headers, data=json.dumps(payload_atividade))

        if response.status_code in [200, 201]:
            st.success("✅ Requisição à API principal bem-sucedida.")
            fragmentos = response.json()
            atividade_texto = "".join([frag['text'] for frag in fragmentos])

            # Processamento com a API Groq
            client = Groq(api_key=groq_api_key)
            completion = client.chat.completions.create(
                model="llama3-8b-8192",
                messages=[{
                    "role": "user",
                    "content": f"""
                    Baseado nas informações fornecidas a seguir, crie uma atividade de matemática detalhada, com um passo a passo claro, que possa ser utilizada por um professor do ensino fundamental. A atividade deve incluir:
                    - Introdução e contexto da atividade.
                    - Descrição detalhada dos passos que os alunos devem seguir.
                    - Perguntas desafiadoras que incentivem o pensamento crítico.
                    - Explicações claras para ajudar na resolução das questões.
                    - Dicas ou observações importantes para o professor.

                    Informações fornecidas: {atividade_texto}

                    Formato da resposta esperado:
                    1. **Introdução**
                    2. **Passo 1: [Descrição]**
                    - Pergunta: [Exemplo de questão]
                    - Dica: [Dica para o professor]
                    3. **Passo 2: [Descrição]**
                    - Pergunta: [Exemplo de questão]
                    - Dica: [Dica para o professor]
                    4. **Conclusão e observações finais**
                    """
                }],
                temperature=0.7,
                max_tokens=1500,
                top_p=1,
                stream=True,
                stop=None
            )

            st.write("### ✨ Atividade Final")
            resposta_final = ""
            for chunk in completion:
                if hasattr(chunk, 'choices') and chunk.choices[0].delta.content:
                    resposta_final += chunk.choices[0].delta.content

            # Exibição da resposta com formatação visual
            st.markdown(
                f"""
                <div style="background-color:#f0f8ff; padding:15px; border-radius:10px;">
                <h3 style="color:#2a9d8f;">📝 Resultado da Atividade:</h3>
                <p style="font-size:16px; color:#264653;">{resposta_final}</p>
                </div>
                """, 
                unsafe_allow_html=True
            )

        else:
            st.error("❌ Erro ao fazer a requisição à API principal. Verifique as credenciais e tente novamente.")
    else:
        st.warning("⚠️ Por favor, insira as credenciais da API para continuar.")
