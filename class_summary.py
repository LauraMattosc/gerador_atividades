import streamlit as st
import pandas as pd
import datetime

# Function to simulate fetching data
@st.cache_data
def fetch_data():
    teacher = {'name': 'Prof. Silva'}
    school = {'name': 'Escola Futuro Brilhante'}
    class_data = {'name': 'Turma A', 'year': '2023'}
    students = pd.DataFrame({
        'name': ['Alice', 'Bruno', 'Carla', 'Daniel'],
        'hypothesis': ['A', 'B', 'A', 'C'],
        'comment': ['Progresso excelente', None, 'Precisa de mais apoio', 'Esforço consistente']
    })
    return teacher, school, class_data, students

# Helper function to get background color based on hypothesis
@st.cache_data
def get_background_color(acronym):
    color_map = {'A': '#FFD700', 'B': '#ADFF2F', 'C': '#FF69B4', 'NA': '#E3E4E5'}
    return color_map.get(acronym, '#E3E4E5')

# Fetch data
teacher, school, class_data, students = fetch_data()

# Page setup
st.set_page_config(page_title='Painel da Classe', layout='centered')
st.title("Painel da Classe")

# Display teacher and school info
st.subheader("Informações da Classe")
st.write(f"**Professor(a):** {teacher['name']}")
st.write(f"**Escola:** {school['name']}")
st.write(f"**Turma e Ano:** {class_data['name']} - {class_data['year']}")

# Display current date
current_month = datetime.datetime.now().strftime("%B de %Y")
st.write(f"**Data da Sondagem:** {current_month}")

# Display hypotheses summary
def group_by_hypotheses(students_df):
    return students_df.groupby('hypothesis').size().reset_index(name='Quantidade de Alunos')

grouped_hypotheses = group_by_hypotheses(students)
st.subheader("Resumo das Hipóteses")
st.table(grouped_hypotheses)

# Display student list
def render_student_table(students_df):
    for _, row in students_df.iterrows():
        st.write(f"**Nome:** {row['name']}")
        st.markdown(
            f"<div style='background-color: {get_background_color(row['hypothesis'])}; padding: 5px; border-radius: 5px; display: inline-block;'>"
            f"{row['hypothesis']}</div>", unsafe_allow_html=True)
        if row['comment']:
            with st.expander("Ver Comentário"):
                st.write(f"{row['comment']}")

st.subheader("Lista de Alunos")
render_student_table(students)

# Placeholder for PDF download
if st.button("Baixar PDF"):
    st.write("Lógica para geração de PDF aqui.")

# Link for further resources
st.markdown("[Minhas Sondagens](#)", unsafe_allow_html=True)
