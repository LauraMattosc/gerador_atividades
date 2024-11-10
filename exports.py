import streamlit as st
from fpdf import FPDF
import datetime

# Função para gerar o PDF do plano de aula
def generate_pdf(content: str, filename: str):
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    
    pdf.set_font("Arial", size=12)
    
    # Adiciona o conteúdo ao PDF
    pdf.multi_cell(0, 10, content)
    
    # Salva o PDF com o nome do arquivo
    pdf.output(filename)

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

# Função principal para exibir os botões
def main():
    st.title("Gerador de Plano de Aula")
    
    # Exemplo de entrada de dados para o plano de aula
    componente = "Matemática"
    unidade_tematica = "Leitura"
    objetivo_conhecimento = "Compreensão em Leitura"
    current_month = datetime.datetime.now().strftime("%B de %Y")
    perfis_turma = "Perfil detalhado da turma"

    # Gerar o plano de aula
    plano_aula = generate_lesson_plan(componente, unidade_tematica, objetivo_conhecimento, current_month, perfis_turma)

    # Exibir o plano de aula
    st.subheader("Plano de Aula Gerado")
    st.text_area("Plano de Aula", plano_aula, height=300)

    # Botão para editar o plano
    if st.button("✏️ Editar Plano"):
        plano_aula_editado = st.text_area("Edite o plano de aula:", plano_aula, height=300)
    
    # Botão para baixar o PDF
    if st.button("📥 Baixar PDF"):
        # Salvar o conteúdo do plano de aula gerado em PDF
        generate_pdf(plano_aula, "plano_aula.pdf")
        st.success("PDF gerado com sucesso!")
    
    # Botão para salvar o plano de aula em um arquivo
    if st.button("💾 Salvar"):
        # Criar um arquivo de texto com o conteúdo do plano de aula
        with open("plano_aula.txt", "w") as file:
            file.write(plano_aula)
        st.success("Plano de aula salvo com sucesso!")

    # Exibindo o botão para download do arquivo
    with open("plano_aula.txt", "r") as file:
        st.download_button("Baixar Plano de Aula em Texto", file, "plano_aula.txt")

if __name__ == "__main__":
    main()
