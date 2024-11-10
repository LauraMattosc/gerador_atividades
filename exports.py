import streamlit as st
import json
import datetime
from fpdf import FPDF

# Caminho do arquivo JSON para armazenar os planos
JSON_FILE = "plano_aula.json"

# Função para salvar o plano de aula em JSON
def save_plan_to_json(plan: str):
    try:
        with open(JSON_FILE, "w") as file:
            json.dump({"plano_aula": plan}, file)
        st.success("Plano de aula salvo com sucesso!")
    except Exception as e:
        st.error(f"Erro ao salvar o plano: {e}")

# Função para carregar o último plano de aula do arquivo JSON
def load_last_plan():
    try:
        with open(JSON_FILE, "r") as file:
            data = json.load(file)
            return data.get("plano_aula", "")
    except FileNotFoundError:
        return ""  # Se o arquivo não existir, retorna uma string vazia
    except json.JSONDecodeError:
        return ""  # Se o JSON estiver corrompido, retorna uma string vazia

# Função para gerar o plano de aula formatado
def generate_lesson_plan(componente, unidade_tematica, objetivo_conhecimento, current_month, perfis_turma):
    """
    Gera o plano de aula com base nos dados fornecidos (simulação de conteúdo).
    """
    plan = f"""
    Plano de Aula:
    Componente: {componente}
    Unidade Temática: {unidade_tematica}
    Objetivo de Conhecimento: {objetivo_conhecimento}
    Mês: {current_month}
    Perfis da Turma: {perfis_turma}

    Conteúdo Programático:
    - Introdução ao tema
    - Atividades práticas
    - Discussão em grupo
    - Avaliação final
    """
    return plan

# Função para gerar o PDF do plano de aula
def generate_pdf(content: str):
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    
    pdf.set_font("Arial", size=12)
    
    # Adiciona o conteúdo ao PDF
    pdf.multi_cell(0, 10, content)
    
    # Salva o PDF com o nome do arquivo
    pdf_filename = "plano_aula.pdf"
    pdf.output(pdf_filename)

    return pdf_filename

# Função principal para exibir os botões
def main():
    st.title("Gerador de Plano de Aula")
    
    # Exemplo de entrada de dados para o plano de aula
    componente = "Matemática"
    unidade_tematica = "Leitura"
    objetivo_conhecimento = "Compreensão em Leitura"
    current_month = datetime.datetime.now().strftime("%B de %Y")
    perfis_turma = "Perfil detalhado da turma"
    
    # Carrega o último plano de aula salvo
    plano_aula = load_last_plan()
    
    if not plano_aula:
        # Se não houver um plano salvo, gera um plano padrão
        plano_aula = generate_lesson_plan(componente, unidade_tematica, objetivo_conhecimento, current_month, perfis_turma)

    # Exibir o plano de aula
    st.subheader("Plano de Aula Gerado")
    plano_aula_editado = st.text_area("Plano de Aula", plano_aula, height=300)

    # Botão para editar o plano
    if st.button("✏️ Editar Plano"):
        plano_aula_editado = st.text_area("Edite o plano de aula:", plano_aula, height=300)
    
    # Botão para baixar o PDF
    if st.button("📥 Baixar PDF"):
        # Salvar o conteúdo do plano de aula gerado em PDF
        pdf_filename = generate_pdf(plano_aula_editado)
        with open(pdf_filename, "rb") as pdf_file:
            st.download_button("Baixar PDF", pdf_file, file_name=pdf_filename)
        st.success("PDF gerado com sucesso!")
    
    # Botão para salvar o plano de aula em um arquivo JSON
    if st.button("💾 Salvar"):
        save_plan_to_json(plano_aula_editado)
    
    # Exibindo o botão para download do arquivo de texto
    st.download_button("Baixar Plano de Aula em Texto", plano_aula_editado, file_name="plano_aula.txt")

if __name__ == "__main__":
    main()
