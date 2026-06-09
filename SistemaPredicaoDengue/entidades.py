from dataclasses import dataclass
from datetime import date
from typing import Optional

@dataclass
class RegistroCaso:
    """Um caso confirmado/notificado de dengue pelo SINAN."""
    id_caso: int
    distrito: str
    data_notificacao: date
    unidade_saude: str
    semana_epidemiologica: int
    mes: int
    contagem_casos: int = 1

@dataclass
class RegistroClima:
    """Uma observação climática de uma estação do INMET."""
    id_estacao: str
    data: date
    semana_epidemiologica: int
    distrito: str
    temperatura_media: float
    temperatura_maxima: float
    precipitacao: float
    umidade: float
    latitude: Optional[float] = None
    longitude: Optional[float] = None

@dataclass
class Previsao:
    """Uma previsão matemática do modelo para um distrito e semana específicos."""
    distrito: str
    semana_epidemiologica: int
    ano: int
    casos_previstos: float
    nome_modelo: str
