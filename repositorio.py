from typing import List
from domain.entidades import RegistroCaso, RegistroClima
from domain.resultado_previsao import ResultadoPrevisao
from utils.excecoes import ErroConexaoBD

class Repositorio:
    """Lê/escreve os objetos de domínio no MySQL via um ConectorBD."""

    def __init__(self, conector_bd, configuracao) -> None:
        self.conector_bd = conector_bd
        self.configuracao = configuracao

    def salvar_previsoes(self, resultados: List[ResultadoPrevisao]) -> None:
        """Salva a lista de previsões geradas pela IA no banco de dados."""
        if not resultados:
            return

        conexao = self.conector_bd.conectar_mysql(self.configuracao)
        try:
            self._garantir_tabelas_existem(conexao)
            cursor = conexao.cursor()
            cursor.executemany(
                """
                INSERT INTO tb_previsoes
                    (periodo, nome_modelo, estimativa, ic_inferior, ic_superior)
                VALUES (%s, %s, %s, %s, %s)
                """,
                [
                    (
                        r.periodo, r.nome_modelo, float(r.estimativa),
                        None if r.intervalo_confianca is None else float(r.intervalo_confianca[0]),
                        None if r.intervalo_confianca is None else float(r.intervalo_confianca[1]),
                    )
                    for r in resultados
                ],
            )
            conexao.commit()
            cursor.close()
            
        except Exception as exc:
            conexao.rollback()
            raise ErroConexaoBD(f"Falha ao salvar as previsões: {exc}") from exc
        finally:
            conexao.close()

    def salvar_dados_historicos(self, registros: List) -> None:
        """Salva as linhas dos arquivos CSV (Casos e Clima) no banco de dados."""
        casos = [r for r in registros if isinstance(r, RegistroCaso)]
        clima = [r for r in registros if isinstance(r, RegistroClima)]
        
        if not casos and not clima:
            return

        conexao = self.conector_bd.conectar_mysql(self.configuracao)
        try:
            self._garantir_tabelas_existem(conexao)
            cursor = conexao.cursor()
            
            if casos:
                cursor.executemany(
                    """
                    INSERT INTO tb_historico_casos
                        (id_caso, distrito, data_notificacao, unidade_saude,
                         semana_epidemiologica, mes, contagem_casos)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                    """,
                    [(r.id_caso, r.distrito, r.data_notificacao, r.unidade_saude, 
                      r.semana_epidemiologica, r.mes, r.contagem_casos) for r in casos]
                )
                
            if clima:
                cursor.executemany(
                    """
                    INSERT INTO tb_clima
                        (id_estacao, data_observacao, semana_epidemiologica, distrito,
                         temperatura_media, temperatura_maxima, precipitacao, umidade,
                         latitude, longitude)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    """,
                    [(r.id_estacao, r.data, r.semana_epidemiologica, r.distrito,
                      self._nan_para_nulo(r.temperatura_media),
                      self._nan_para_nulo(r.temperatura_maxima),
                      self._nan_para_nulo(r.precipitacao),
                      self._nan_para_nulo(r.umidade),
                      r.latitude, r.longitude) for r in clima]
                )
            
            conexao.commit()
            cursor.close()
            
        except Exception as exc:
            conexao.rollback()
            raise ErroConexaoBD(f"Falha ao salvar os dados históricos: {exc}") from exc
        finally:
            conexao.close()

    def _garantir_tabelas_existem(self, conexao) -> None:
        """Cria as tabelas caso seja a primeira vez que o sistema está rodando."""
        cursor = conexao.cursor()
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS tb_historico_casos (
                id INT AUTO_INCREMENT PRIMARY KEY,
                id_caso INT,
                distrito VARCHAR(120),
                data_notificacao DATE,
                unidade_saude VARCHAR(200),
                semana_epidemiologica INT,
                mes INT,
                contagem_casos INT
            )
        """)
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS tb_clima (
                id INT AUTO_INCREMENT PRIMARY KEY,
                id_estacao VARCHAR(80),
                data_observacao DATE,
                semana_epidemiologica INT,
                distrito VARCHAR(120),
                temperatura_media DOUBLE,
                temperatura_maxima DOUBLE,
                precipitacao DOUBLE,
                umidade DOUBLE,
                latitude DOUBLE,
                longitude DOUBLE
            )
        """)
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS tb_previsoes (
                id INT AUTO_INCREMENT PRIMARY KEY,
                periodo VARCHAR(120),
                nome_modelo VARCHAR(80),
                estimativa DOUBLE,
                ic_inferior DOUBLE NULL,
                ic_superior DOUBLE NULL,
                criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        cursor.close()

    @staticmethod
    def _nan_para_nulo(valor):
        """Converte números vazios (NaN) do Python para formato Nulo do MySQL."""
        if isinstance(valor, float) and valor != valor:
            return None
        return valor
