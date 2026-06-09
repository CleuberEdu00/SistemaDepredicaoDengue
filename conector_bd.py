import mysql.connector
from mysql.connector import Error as ErroMySQL
from utils.excecoes import ErroConexaoBD

class ConectorBD:
    """Abre conexões nativas com o MySQL lendo as Configurações."""

    def conectar_mysql(self, configuracao) -> "mysql.connector.connection.MySQLConnection":
        """Retorna a conexão com o banco de dados e trata falhas."""
        try:
            conexao = mysql.connector.connect(
                host=configuracao.host_mysql,
                port=configuracao.porta_mysql,
                database=configuracao.banco_mysql,
                user=configuracao.usuario_mysql,
                password=configuracao.senha_mysql,
                autocommit=False,
            )
            if not conexao.is_connected():
                raise ErroConexaoBD("O MySQL informou que a conexão não está ativa.")
            
            return conexao
            
        except ErroMySQL as exc:
            raise ErroConexaoBD(
                f"Não foi possível conectar ao MySQL em {configuracao.host_mysql}:{configuracao.porta_mysql}: {exc}"
            ) from exc
