import os
import sys
import subprocess

def verificar_estrutura_projeto():
    estrutura_esperada = [
        'api_requests.py',
        'app.py',
        '.streamlit/secrets.toml'
    ]

    for item in estrutura_esperada:
        if not os.path.exists(item):
            print(f"❌ Arquivo ou diretório não encontrado: {item}")
            return False
    print("✅ Estrutura do projeto está correta.")
    return True

def verificar_dependencias():
    dependencias = [
        'streamlit',
        'pandas',
        'matplotlib',
        'requests',
        'groq',
        'altair'
    ]

    todas_instaladas = True
    for dependencia in dependencias:
        try:
            __import__(dependencia)
            print(f"✅ Dependência instalada: {dependencia}")
        except ImportError:
            print(f"❌ Dependência não instalada: {dependencia}")
            todas_instaladas = False

    return todas_instaladas

def verificar_secrets():
    secrets_path = '.streamlit/secrets.toml'
    if not os.path.exists(secrets_path):
        print(f"❌ Arquivo de credenciais não encontrado: {secrets_path}")
        return False

    try:
        import toml
        with open(secrets_path, 'r') as f:
            secrets = toml.load(f)
        if 'api' in secrets and 'api_token' in secrets['api'] and 'groq_api_key' in secrets['api']:
            print("✅ Credenciais encontradas no arquivo secrets.toml.")
            return True
        else:
            print("❌ Credenciais não encontradas ou incompletas no arquivo secrets.toml.")
            return False
    except Exception as e:
        print(f"❌ Erro ao ler o arquivo secrets.toml: {e}")
        return False

def main():
    print("🔍 Verificando a estrutura do projeto...")
    estrutura_ok = verificar_estrutura_projeto()

    print("\n🔍 Verificando as dependências...")
    dependencias_ok = verificar_dependencias()

    print("\n🔍 Verificando o arquivo de credenciais...")
    secrets_ok = verificar_secrets()

    if estrutura_ok and dependencias_ok and secrets_ok:
        print("\n✅ Todas as verificações foram concluídas com sucesso. O projeto está configurado corretamente.")
    else:
        print("\n❌ Algumas verificações falharam. Por favor, corrija os problemas listados acima e tente novamente.")

if __name__ == "__main__":
    main()
