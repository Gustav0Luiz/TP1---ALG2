import math

class Node:
	def __init__(self, point, left=None, right=None):
		self.point = point
		self.left = left
		self.right = right

class KDTree:
	def __init__(self, points):
		self.root = self._build(points)

	def _build(self, points, depth=0):
		if not points:
			return None

		# Determinar qual é o número de dimensões da árvore
		k = len(points[0])
		# Determinar o axis conforme o depth da recursão
		axis = depth % k

		# Ordenar os pontos pelo axis e escolher o ponto mediano
		points.sort(key=lambda x: x[axis])
		median_idx = len(points) // 2

		# Criar nó e construir recursivamente as subárvores
		return Node(
			point=points[median_idx],
			left=self._build(points[:median_idx], depth + 1),
			right=self._build(points[median_idx + 1:], depth + 1)
		)

	def display(self, node=None, depth=0):
		if node is None:
			node = self.root
		
		print("  " * depth + f"Axis {depth % len(node.point)}: {node.point}")
		
		if node.left:
			self.display(node.left, depth + 1)
		if node.right:
			self.display(node.right, depth + 1)
   
   # ____________ Buscas ____________
   
	def search_rect(self, point_min, point_max):
		results = []
		self._rect_query(self.root, point_min, point_max, 0, results)
		return results

	def _rect_query(self, node, p_min, p_max, depth, results):
		if node is None:
			return

		k = len(node.point)
		axis = depth % k

		# Checar se o ponto do nó atual está dentro do retângulo
		if all(p_min[i] <= node.point[i] <= p_max[i] for i in range(k)):
			results.append(node.point)

		# Poda da árvore: checar qual caminho seguir
		if p_min[axis] < node.point[axis]:
			self._rect_query(node.left, p_min, p_max, depth + 1, results)
		if p_max[axis] >= node.point[axis]:
			self._rect_query(node.right, p_min, p_max, depth + 1, results)

	def search_radius(self, center, radius):
		results = []
		self._radius_query(self.root, center, radius, 0, results)
		return results

	def _radius_query(self, node, center, radius, depth, results):
		if node is None:
			return

		k = len(node.point)
		axis = depth % k

		# Calcular distância euclidiana
		dist = math.sqrt(sum((node.point[i] - center[i])**2 for i in range(k)))
		
		# Checar se o ponto do nó atual está dentro do raio
		if dist <= radius:
			results.append(node.point)

		# Poda da árvore: checar qual caminho seguir
		diff = center[axis] - node.point[axis]
		if diff - radius < 0: 
			self._radius_query(node.left, center, radius, depth + 1, results)
		if diff + radius >= 0:
			self._radius_query(node.right, center, radius, depth + 1, results)

# Depuração
if __name__ == "__main__":
	import pandas as pd
	from pathlib import Path
	
	PROJECT_ROOT = Path(__file__).parent.parent
	COORDS_PATH = PROJECT_ROOT / 'data' / 'butecos_bh_coords.csv'
	
	sample_coords = pd.read_csv(COORDS_PATH)
	tree = KDTree(sample_coords[['latitude', 'longitude']].values.tolist())
	#tree.display()
 
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

		bounds = [
			[lat_centro - delta_lat, lon_centro - delta_lon],  # canto inferior esquerdo
			[lat_centro + delta_lat, lon_centro + delta_lon]   # canto superior direito
		]
		return bounds
 
 
	LAT = -19.922760
	LON = -43.945162
	radious = 3 # km
 
	bounds = calcular_limites_retangulo(LAT, LON, radious)
	print(bounds)
	print(tree.search_rect(bounds[0], bounds[1]))
	