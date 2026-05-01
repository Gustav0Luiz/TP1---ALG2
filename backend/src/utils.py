import math

def calcular_limites_retangulo(lat_centro, lon_centro, diagonal_km):
    # o retangulo eh um quadrado
    lado_km = diagonal_km / math.sqrt(2)  # (D = L * raiz(2))
    meio_lado_km = lado_km / 2 # tamanho para cada lado do centro

    # Aproximação:
    # 1 grau de latitude equivale a aproximadamente 111km
    delta_lat = meio_lado_km / 111

    # 1 grau de longitude varia conforme a latitude - vide formula:
    # 1 km =  111.32 * cos(latitude_em_radianos)
    delta_lon = meio_lado_km / (111.32 * math.cos(math.radians(lat_centro)))

    bounds = (
        (lat_centro - delta_lat, lon_centro - delta_lon),  # canto inferior esquerdo
        (lat_centro + delta_lat, lon_centro + delta_lon)   # canto superior direito
    )
    return bounds