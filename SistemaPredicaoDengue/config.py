import os
from dataclasses import dataclass, field

@dataclass
class Configuracao:
    """Classe responsável por carregar as configurações via variáveis de ambiente."""

    host_mysql: str = field(default_factory=lambda: os.environ.get("MYSQL_HOST", "localhost"))
    porta_mysql: int = field(default_factory=lambda: int(os.environ.get("MYSQL_PORT", "3306")))
    banco_mysql: str = field(default_factory=lambda: os.environ.get("MYSQL_DATABASE", "dengue_db"))
    usuario_mysql: str = field(default_factory=lambda: os.environ.get("MYSQL_USER", "dengue_user"))
    senha_mysql: str = field(default_factory=lambda: os.environ.get("MYSQL_PASSWORD", "dengue_pass"))
    
    modo_pipeline: str = field(default_factory=lambda: os.environ.get("PIPELINE_MODE", "train"))
    tipo_modelo: str = field(default_factory=lambda: os.environ.get("MODEL_TYPE", "xgboost"))
    diretorio_dados: str = field(default_factory=lambda: os.environ.get("DATA_DIR", "data"))
    diretorio_modelo: str = field(default_factory=lambda: os.environ.get("MODEL_DIR", "model_store"))

    @classmethod
    def carregar_do_ambiente(cls) -> "Configuracao":
        """Construtor que inicializa a classe pegando os valores padrão."""
        return cls()
