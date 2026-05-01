import math

def calcular_limites_retangulo(lat_centro, lon_centro, diagonal_km):
    """
    Calcula os limites do retângulo a partir da diagonal informada.

    O retângulo é tratado como um quadrado centralizado no endereço.
    """

    lado_km = diagonal_km / math.sqrt(2)
    meio_lado_km = lado_km / 2

    delta_lat = meio_lado_km / 111.32
    delta_lon = meio_lado_km / (111.32 * math.cos(math.radians(lat_centro)))

    bounds = (
        (lat_centro - delta_lat, lon_centro - delta_lon),
        (lat_centro + delta_lat, lon_centro + delta_lon)
    )

    return bounds

def estimar_raio_graus(lat_centro, distancia_km):
	delta_lat = distancia_km / 111.32
	delta_lon = distancia_km / (111.32 * math.cos(math.radians(lat_centro)))
	return max(delta_lat, delta_lon)

def calcular_distancia_km(coords1:tuple, coords2:tuple):
	lat1, lon1 = coords1
	lat2, lon2 = coords2

	# Raio médio da Terra em km
	R = 6371.0

	# Converter graus para radianos
	phi1 = math.radians(lat1)
	phi2 = math.radians(lat2)
	delta_phi = math.radians(lat2 - lat1)
	delta_lambda = math.radians(lon2 - lon1)

	# Fórmula de Haversine
	a = math.sin(delta_phi / 2)**2 + math.cos(phi1) * math.cos(phi2) * math.sin(delta_lambda / 2)**2
	c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
	distancia = R * c
	
	return distancia