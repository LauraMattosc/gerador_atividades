
# Sistema de Alfabetização e Planejamento de Aulas - AlfaTutor

## Descrição

O **AlfaTutor** é uma ferramenta interativa desenvolvida para ajudar os professores no processo de alfabetização e no planejamento de aulas. Utilizando a interface **Streamlit**, o sistema permite que os docentes visualizem o desempenho dos alunos, criem atividades educativas personalizadas e gerem planos de aula detalhados. A plataforma integra diferentes tecnologias de IA, como **Groq** e **Whisper**, para facilitar o ensino e a personalização do aprendizado.

## Funcionalidades

### 1. **Visualização de Dados da Turma**
O painel exibe informações detalhadas sobre o desempenho dos alunos, agrupados por **hipóteses de escrita**. Isso inclui gráficos e tabelas que permitem aos professores entenderem o progresso da turma e identificar áreas de melhoria.

### 2. **Explicações das Hipóteses de Escrita**
O sistema fornece explicações detalhadas sobre as diferentes **hipóteses de escrita** com base no desenvolvimento da alfabetização dos alunos. As hipóteses são:

- **Pré-silábica**
- **Silábico sem valor sonoro**
- **Silábico com valor sonoro**
- **Silábico-alfabética**
- **Alfabética**

Essas explicações ajudam os professores a monitorar e guiar o desenvolvimento da escrita de seus alunos.

### 3. **Gerador de Atividades**
O sistema permite gerar atividades personalizadas de acordo com o nível de dificuldade e o tema desejado. As atividades são geradas dinamicamente com base em um conjunto de dados e APIs, como o modelo **Groq**, permitindo uma experiência adaptativa e interativa.

### 4. **Plano de Aula Inteligente**
O **AlfaTutor** utiliza um modelo de IA para gerar planos de aula completos, considerando o componente curricular, unidade temática e os objetivos de conhecimento. Isso garante que os planos de aula sejam detalhados e otimizados de acordo com o nível de alfabetização da turma.

### 5. **Integração com WhatsApp**
O sistema permite interação com alunos e professores via **WhatsApp**, utilizando a plataforma **Turn** para enviar e receber mensagens, garantindo um canal eficiente de comunicação.

## Arquitetura do Sistema

O sistema segue uma arquitetura de três camadas principais:

1. **Bancos de Dados**: Armazenamento das informações dos alunos, desempenho e planos de aula. Utiliza **MySQL** e **PostgreSQL (PG)**.
2. **LLMs e APIs**:
   - **Groq**: O modelo Groq processa e gera respostas para os prompts de planejamento de aula.
   - **Whisper API**: Transcrição de áudio para texto, permitindo interações por voz.
   - **Anvil**: Python-based drag-and-drop web app builder.
3. **Interface**:
   - **Streamlit**: Interface interativa que permite visualização de dados e interação com o sistema.
   - **WhatsApp via Turn**: Plataforma de comunicação com os usuários.

## Fluxo de Dados

O fluxo de dados começa com os **bancos de dados**, onde as informações da turma são armazenadas. As interações com o sistema, como análise de desempenho e a geração de atividades, são processadas através dos **modelos de linguagem** como o **Groq** e **Whisper** para transcrição de áudio. O sistema então exibe os resultados através da interface **Streamlit**, ou envia notificações via **WhatsApp**.

## Tecnologias Utilizadas

- **Streamlit**: Framework para criar interfaces interativas em Python.
- **Pandas**: Biblioteca para análise de dados.
- **Matplotlib**: Para gerar gráficos interativos.
- **APIs**:
  - **Groq**: Para geração de planos de aula detalhados.
  - **Whisper**: Para transcrição de áudio em texto.
  - **Turn**: Plataforma de integração com o WhatsApp.

## Como Usar

### 1. Clonando o Repositório

Clone o repositório para o seu ambiente local:

```bash
git clone https://github.com/seu_usuario/alfatutor.git
cd alfatutor
```

### 2. Instalando as Dependências

Instale as dependências necessárias com o **pip**:

```bash
pip install -r requirements.txt
```

### 3. Rodando o Aplicativo

Para rodar o aplicativo **Streamlit**, execute:

```bash
streamlit run app.py
```

### 4. Configuração das Credenciais

Certifique-se de configurar a chave da **API Groq** no arquivo `secrets.toml`.

### 5. Interação com o Sistema

- **Visualizar a Turma**: Escolha a turma e visualize gráficos de desempenho.
- **Gerar Atividades**: Selecione o tema e nível de dificuldade para gerar atividades.
- **Gerar Planos de Aula**: O sistema usa IA para gerar planos personalizados.

## Base de Dados de Planos de Aula

A base de dados do **AlfaTutor** contém mais de **6.000 planos de aula** que servem como insumo para o processo de geração de novos planos. Para a demonstração, essa base foi recortada, oferecendo uma versão reduzida com exemplos de planos. Esses dados ajudam a IA a gerar planos de aula mais precisos e específicos, adaptados às necessidades da turma.

## Exemplo de Interface

Aqui está um exemplo da arquitetura do **AlfaTutor** se apresenta para os professores:

(arquitetura.png)

**GIF da Demonstração da Interface:**

(chrome-capture-2024-11-10 (1).gif)

## Contribuições

Este projeto está aberto para contribuições. Para contribuir, siga os passos abaixo:

1. Faça um **fork** do repositório.
2. Crie uma **nova branch** para suas alterações.
3. **Commit** suas alterações.
4. Envie para o repositório remoto.
5. Abra um **Pull Request** explicando as mudanças.

## Licença

Este projeto está licenciado sob a **MIT License**. Consulte o arquivo [LICENSE](LICENSE) para mais detalhes.

## Contato

Se você tiver dúvidas ou sugestões, entre em contato:

---

Obrigado por usar o **AlfaTutor**! Estamos sempre em busca de melhorar e adicionar novas funcionalidades.
