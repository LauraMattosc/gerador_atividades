import os

# Estrutura esperada do projeto
estrutura_esperada = {
    '': ['api_requests.py', 'app.py', '.streamlit'],
    '.streamlit': ['secrets.toml']
}

def verificar_estrutura(base_path='.'):
    for caminho, arquivos_esperados in estrutura_esperada.items():
        caminho_completo = os.path.join(base_path, caminho) if caminho else base_path
        
        # Verifica se o caminho existe
        if not os.path.exists(caminho_completo):
            print(f"Erro: O caminho '{caminho_completo}' não existe.")
            continue

        # Verifica se é um diretório
        if os.path.isdir(caminho_completo):
            arquivos_no_diretorio = os.listdir(caminho_completo)
            
            # Verifica os arquivos esperados
            for arquivo in arquivos_esperados:
                if arquivo not in arquivos_no_diretorio:
                    print(f"Erro: O arquivo '{arquivo}' não foi encontrado em '{caminho_completo}'.")
                else:
                    print(f"OK: O arquivo '{arquivo}' está presente em '{caminho_completo}'.")
        else:
            print(f"Erro: '{caminho_completo}' não é um diretório.")

if __name__ == "__main__":
    verificar_estrutura()
