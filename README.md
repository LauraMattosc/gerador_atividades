# 🛠️ Gerador de Atividades Personalizadas com APIs Externas

Este projeto é um aplicativo de Streamlit que utiliza APIs externas para gerar atividades detalhadas e personalizadas. O fluxo de trabalho integra duas APIs principais para criar conteúdos envolventes e relevantes para diferentes finalidades, como a criação de atividades educacionais.

## 🚀 Funcionalidades Principais

- **Geração de conteúdos personalizados** utilizando uma API de busca de fragmentos de texto e a API Groq para processamento avançado com modelos de IA.
- **Interface de usuário intuitiva** em Streamlit, permitindo a inserção de credenciais e a customização das atividades.
- **Suporte a diferentes temas e níveis de dificuldade**, ajustando o conteúdo para atender necessidades variadas.

## 🛠️ Tecnologias Utilizadas

- **Python**: Linguagem de programação para a lógica do projeto.
- **Streamlit**: Framework para a criação da interface web interativa.
- **Groq API**: Integração com o modelo LLaMA para processamento e geração de conteúdo.
- **Requests**: Biblioteca para realizar chamadas HTTP.
- **HTML e CSS**: Para estilização da exibição do conteúdo no Streamlit.

## 🔄 Fluxo de Trabalho

1. **Entrada de credenciais**:
   - O usuário insere o token de autenticação da API principal e a chave da API Groq diretamente na interface.

2. **Seleção de tema e dificuldade**:
   - O usuário escolhe o tema da atividade e o nível de dificuldade a partir de menus suspensos no Streamlit.

3. **Requisição à API de fragmentos de texto**:
   - A aplicação envia um payload à API `https://ragne.codebit.dev/rag/text-fragments` com uma solicitação para obter fragmentos de texto relacionados ao tema selecionado.
   - A API principal retorna uma série de fragmentos de texto que serão usados como base para a atividade.

4. **Processamento com a API Groq**:
   - Os fragmentos de texto são processados com o modelo LLaMA da Groq para gerar uma atividade completa e bem estruturada.
   - O prompt é criado dinamicamente para que a IA elabore uma atividade que inclui introdução, passo a passo detalhado, perguntas e dicas para professores.

5. **Exibição do resultado**:
   - O resultado gerado pela API Groq é exibido de forma estilizada na interface do Streamlit.

## 🧑‍🏫 Como Usar

1. **Clone este repositório**:

   ```bash
   git clone https://github.com/seuusuario/gerador-atividades.git
   cd gerador-atividades
# Guia de Início Rápido

## 1. Clone este repositório:

  ```bash
    git clone https://github.com/seuusuario/gerador-atividades.git
```

## 2. Instale as dependências:
  ```bash
  pip install -r requirements.txt
```

3. Execute o aplicativo:
  ```bash
    streamlit run app.py
```
Notas Importantes:
- Certifique-se de ter o Python e o pip instalados em sua máquina antes de executar os comandos.
- Para executar o aplicativo, será necessário fornecer suas credenciais de API quando solicitado pelo aplicativo Streamlit.
- Verifique se suas chaves de API estão configuradas corretamente para garantir o funcionamento completo do aplicativo.
