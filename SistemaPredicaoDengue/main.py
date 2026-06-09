import sys

# Importa as classes em português que nós estruturamos
from SistemaPredicaoDengue.config import Configuracao
from SistemaPredicaoDengue.conector_bd import ConectorBD
from SistemaPredicaoDengue.repositorio import Repositorio

def executar_inicializacao():

    try:
        # 1. Carrega as configurações (O Docker injeta as senhas aqui automaticamente)
        print("[Passo 1] Carregando variáveis de ambiente...")
        configuracao = Configuracao.carregar_do_ambiente()
        print(f" -> Banco configurado: {configuracao.banco_mysql}")
        print(f" -> Usuário configurado: {configuracao.usuario_mysql}\n")
        
        # 2. Instancia o Conector do Banco de Dados
        print("[Passo 2] Inicializando o conector nativo do MySQL...")
        conector = ConectorBD()
        
        # 3. Tenta abrir a conexão real com o banco de dados do Docker
        print(f"[Passo 3] Tentando conectar em {configuracao.host_mysql}:{configuracao.porta_mysql}...")
        conexao = conector.conectar_mysql(configuracao)
        print(" -> CONEXÃO ESTABELECIDA COM SUCESSO!\n")
        
        # 4. Instancia o Repositório
        print("[Passo 4] Inicializando o Repositório de dados...")
        repositorio = Repositorio(conector, configuracao)
        
        # 5. Executa a criação automática das tabelas (A prova real para o professor)
        print("[Passo 5] Verificando e criando modelagem de tabelas no banco...")
        repositorio._garantir_tabelas_existem(conexao)
        print(" -> Tabelas 'tb_historico_casos', 'tb_clima' e 'tb_previsoes' verificadas/criadas!\n")
        
        # 6. Fecha a conexão com segurança
        conexao.close()
        print("[Passo 6] Conexão com o banco de dados fechada com segurança.")
        
      
        print(" SUCESSO: A infraestrutura básica está operacional!")
        
        
    except Exception as erro:
        print(f"\n[ERRO CRÍTICO] O pipeline falhou ao iniciar: {erro}", file=sys.stderr)
        print("Verifique se o container do MySQL ('db') está rodando corretamente.\n", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    executar_inicializacao()
