class ErroDadosSINAN(Exception):
    """Gerado quando os dados epidemiológicos de casos (SINAN) não puderem ser lidos."""
    pass

class ErroDadosClima(Exception):
    """Gerado quando os dados climáticos (INMET) não puderem ser lidos."""
    pass

class ErroConexaoBD(Exception):
    """Gerado quando a conexão com o banco falha ou uma consulta SQL dá erro."""
    pass
