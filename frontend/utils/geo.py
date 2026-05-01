"""
utils/geo.py

Responsabilidade do arquivo:
- Centralizar funções geográficas e matemáticas do projeto.
- Calcular distância entre coordenadas.
- Calcular os limites/bounds da área retangular de busca.
- Converter, futuramente, o endereço digitado pelo usuário em latitude/longitude.


- Atualmente algumas funções estão mockadas/simplificadas.
- Depois, CalculateDistance pode ser substituída pela fórmula de Haversine.
- Depois, searchAddress pode ser substituída por uma chamada real à API de geocodificação.
"""

import math
from backend.src.osm import OSMFetcher

_osm_fetcher = OSMFetcher()



def CalculateDistance(lat_origem, lon_origem, lat_destino, lon_destino):
    """
    Calcula a distância entre o ponto de referência e um bar.

    Por enquanto está mockada.
    Depois podemos substituir pela fórmula de Haversine.
    """

    return 1.5


def calcular_limites_retangulo(lat_centro, lon_centro, diagonal_km):
    """
    Calcula os bounds do retângulo.

    Como o usuário fornece apenas a diagonal, assumimos que o retângulo será
    um quadrado centralizado no endereço informado.

    Retorno:
    [
        [latitude_canto_inferior_esquerdo, longitude_canto_inferior_esquerdo],
        [latitude_canto_superior_direito, longitude_canto_superior_direito]
    ]
    """

    # O retângulo será tratado como um quadrado.
    lado_km = diagonal_km / math.sqrt(2)  # D = L * raiz(2)
    meio_lado_km = lado_km / 2  # tamanho para cada lado do centro

    # Aproximação:
    # 1 grau de latitude equivale a aproximadamente 111.32 km.
    delta_lat = meio_lado_km / 111.32

    # 1 grau de longitude varia conforme a latitude.
    # Fórmula aproximada:
    # km_por_grau_longitude = 111.32 * cos(latitude_em_radianos)
    delta_lon = meio_lado_km / (111.32 * math.cos(math.radians(lat_centro)))

    bounds = [
        [lat_centro - delta_lat, lon_centro - delta_lon],  # canto inferior esquerdo
        [lat_centro + delta_lat, lon_centro + delta_lon]   # canto superior direito
    ]

    return bounds


def searchAddress(endereco):
    """
    Converte o endereço digitado pelo usuário em latitude e longitude
    usando OpenStreetMap/Nominatim.
    """

    row = {
        "name": "Endereço buscado",
        "street": endereco,
        "number": "",
        "district": "",
        "city_state": "Belo Horizonte - Minas Gerais",
        "zip_code": ""
    }

    lat, lon = _osm_fetcher.fetch(row, coords_only=True)

    if lat is None or lon is None:
        return None, None

    return float(lat), float(lon)