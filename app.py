# app.py
import streamlit as st
from api_requests import fetch_activity, process_with_groq

# Configuração da interface do Streamlit
def configure_ui():
    """Configura a interface do usuário usando o Streamlit."""
    st.title('🧮 Gerador de Atividades')
    st.write('Este aplicativo cria atividades práticas e envolventes.')

# Entradas principais do usuário
def get_user_inputs():
    """Captura as entradas de dados do usuário."""
    api_token = st.text_input("🔑 Insira seu token de autenticação da API principal:", type="password")
    groq_api_key = st.text_input("🔐 Insira sua chave API do Groq:", type="password")
    tema = st.selectbox("📚 Escolha o tema da atividade:", ["Histórias Curtas", "Completar Palavras", "Sílabas", "Rimas", "Leitura de Palavras"])
    nivel_dificuldade = st.selectbox("🎚️ Selecione o nível de dificuldade:", ["Fácil", "Médio", "Difícil"]) 
    return api_token, groq_api_key, tema, nivel_dificuldade

# Função principal para lidar com a lógica do aplicativo
def main():
    configure_ui()
    api_token, groq_api_key, tema, nivel_dificuldade = get_user_inputs()

    if st.button("Gerar Atividade"):
        if api_token and groq_api_key:
            st.info("🚀 Gerando a atividade, por favor, aguarde...")
            atividade_texto = fetch_activity(api_token, tema, nivel_dificuldade)

            if atividade_texto:
                st.success("✅ Requisição à API principal bem-sucedida.")
                resposta_final = process_with_groq(groq_api_key, atividade_texto)

                if resposta_final:
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
                    st.error("❌ Erro ao processar a atividade com a API Groq.")
            else:
                st.error("❌ Erro ao fazer a requisição à API principal. Verifique as credenciais e tente novamente.")
        else:
            st.warning("⚠️ Por favor, insira as credenciais da API para continuar.")

if __name__ == "__main__":
    main()
