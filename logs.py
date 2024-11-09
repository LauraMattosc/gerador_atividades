import logging
from datetime import datetime
import os

class ActivityLogger:
    """Classe para gerenciar logs das atividades e requisições da API."""
    
    def __init__(self):
        # Criar diretório de logs se não existir
        log_dir = 'logs'
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)
            
        # Nome do arquivo de log com data
        log_file = f'logs/activity_generation_{datetime.now().strftime("%Y%m%d")}.log'
        
        # Configuração básica do logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(message)s',
            handlers=[
                logging.FileHandler(log_file, encoding='utf-8'),
                logging.StreamHandler()  # Para mostrar logs no console também
            ]
        )
        
        self.logger = logging.getLogger(__name__)

    def log_api_request(self, api_name, prompt_length, component, theme):
        """Registra informações sobre a requisição à API."""
        self.logger.info(f"""
        ====== NOVA REQUISIÇÃO API {api_name} ======
        Componente: {component}
        Unidade Temática: {theme}
        Tamanho do Prompt: {prompt_length} caracteres
        Timestamp: {datetime.now().isoformat()}
        =======================================
        """)

    def log_api_response(self, api_name, status_code, response_length):
        """Registra informações sobre a resposta da API."""
        self.logger.info(f"""
        ====== RESPOSTA API {api_name} ======
        Status Code: {status_code}
        Tamanho da Resposta: {response_length} caracteres
        Tempo de Resposta: {datetime.now().isoformat()}
        =======================================
        """)

    def log_error(self, error_type, error_message, additional_info=None):
        """Registra erros detalhados."""
        self.logger.error(f"""
        ====== ERRO DETECTADO ======
        Tipo: {error_type}
        Mensagem: {error_message}
        Informações Adicionais: {additional_info if additional_info else 'N/A'}
        Timestamp: {datetime.now().isoformat()}
        ===========================
        """)

    def log_activity_generation(self, activity_type, success, details=None):
        """Registra informações sobre a geração de atividades."""
        status = "SUCESSO" if success else "FALHA"
        self.logger.info(f"""
        ====== GERAÇÃO DE ATIVIDADE ======
        Tipo: {activity_type}
        Status: {status}
        Detalhes: {details if details else 'N/A'}
        Timestamp: {datetime.now().isoformat()}
        ================================
        """)

    def log_performance_metrics(self, execution_time, memory_usage=None):
        """Registra métricas de performance."""
        self.logger.info(f"""
        ====== MÉTRICAS DE PERFORMANCE ======
        Tempo de Execução: {execution_time:.2f} segundos
        Uso de Memória: {memory_usage if memory_usage else 'N/A'}
        Timestamp: {datetime.now().isoformat()}
        ===================================
        """)

# Exemplo de uso:
logger = ActivityLogger()

# Uso nos métodos existentes:
def process_with_groq(groq_api_key, prompt, componente, unidade_tematica):
    """Processa o texto com a API Groq para gerar uma atividade detalhada."""
    try:
        start_time = datetime.now()
        
        # Log início da requisição
        logger.log_api_request(
            api_name="Groq",
            prompt_length=len(prompt),
            component=componente,
            theme=unidade_tematica
        )

        client = Groq(api_key=groq_api_key)
        completion = client.chat.completions.create(
            model="llama3-8b-8192",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            max_tokens=1500,
            top_p=1,
            stream=True,
            stop=None
        )
        
        resposta_final = ""
        for chunk in completion:
            if hasattr(chunk, 'choices') and chunk.choices[0].delta.content:
                resposta_final += chunk.choices[0].delta.content

        # Log sucesso da resposta
        logger.log_api_response(
            api_name="Groq",
            status_code=200,
            response_length=len(resposta_final)
        )

        # Log métricas de performance
        execution_time = (datetime.now() - start_time).total_seconds()
        logger.log_performance_metrics(execution_time)

        return resposta_final

    except Exception as e:
        # Log erro detalhado
        logger.log_error(
            error_type=type(e).__name__,
            error_message=str(e),
            additional_info={
                "componente": componente,
                "unidade_tematica": unidade_tematica,
                "prompt_length": len(prompt)
            }
        )
        return None

