import streamlit as st
import requests
import base64
from io import BytesIO
from PIL import Image
import toml
from openai import OpenAI
from api_requests import fetch_activity, process_with_groq, generate_activity_with_rag

def load_config(key):
    config = toml.load('credentials.toml')
    return config.get(key, "Not found")

def create_image_ui():
    #st.header("Título")
    if st.button("Gerar Imagem"):
        resposta_final = ''
        with open("resposta_final.txt", "r") as file:
            resposta_final = file.read()

        # Prompt must be length 1000 or les
        groq_api_key = load_config("groq_api_key")
        prompt = f"""Considere o conteúdo a seguir: {resposta_final}. 

        INSTRUÇÕES: Avalie se no conteúdo existem atividades descritas podem ser enriquecidas com uma ilustração ou imagem. 
        Se sim, crie um prompt (com até 1.000 caracteres) adequado para gerar essa imagem na DALL-E.
        """
        new_prompt = process_with_groq(groq_api_key, prompt)
        generate_image(prompt=new_prompt[:1000]) # limitação da DALL-E em 1000 caracteres


def generate_image(prompt):
    openai_api_key = load_config("openai_api_key")
    st.success("Gerando Imagem")
    if prompt:
        try:
            client = OpenAI(api_key=openai_api_key)
            # Generate image using OpenAI API
            response = client.images.generate(
                model="dall-e-2",
                prompt=prompt,
                quality="standard",
                size="1024x1024",
                n=1,
            )

            # Get the image URL from the response
            image_url = response.data[0].url

            # Fetch the image from the URL
            image_response = requests.get(image_url)
            if image_response.status_code == 200:
                image = Image.open(BytesIO(image_response.content))

                # Display the image in Streamlit
                st.image(image, caption='Generated Image', width=400)
            else:
                st.error(f'Error fetching image: {image_response.status_code}')
        except Exception as e:
            st.error(f'Error: {str(e)}')
