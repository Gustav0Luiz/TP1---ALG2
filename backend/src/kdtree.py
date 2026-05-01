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

	def print(self, node=None, depth=0):
		if node is None:
			node = self.root
			if node is None:
				print("Árvore vazia.")
				return
   		
		print("  " * depth + f"Axis {depth % len(node.point)}: {node.point}")
		
		if node.left:
			self.print(node.left, depth + 1)
		if node.right:
			self.print(node.right, depth + 1)
   
   # ____________ Buscas ____________
   
	def search_rect(self, point_min:tuple, point_max:tuple):
		results = []
		if self.root:
			self._rect_query(self.root, point_min, point_max, 0, results)
		return results

	def _rect_query(self, node:Node, p_min:tuple, p_max:tuple,
                 	depth:int, results:list):
		if node is None:
			return

		k = len(node.point)
		axis = depth % k

		# Checar se o ponto do nó atual está dentro do retângulo
		if all(p_min[i] <= node.point[i] <= p_max[i] for i in range(k)):
			results.append(node.point)

		# Poda da árvore: checar qual caminho seguir
		if p_min[axis] < node.point[axis] and node.left:
			self._rect_query(node.left, p_min, p_max, depth + 1, results)
		if p_max[axis] >= node.point[axis] and node.right:
			self._rect_query(node.right, p_min, p_max, depth + 1, results)

	def search_radius(self, center:tuple, radius:float):
		results = []
		if self.root:
			self._radius_query(self.root, center, radius, 0, results)
		return results

	def _radius_query(self, node:Node, center:tuple, radius:float,
                   	depth:int, results:list):
		if node is None:
			return

		k = len(node.point)
		axis = depth % k

		# Calcular distância euclidiana (sqrt(sum((x_i - c_i)^2))))
		dist = math.sqrt(sum((node.point[i] - center[i])**2 for i in range(k)))
		
		# Checar se o ponto do nó atual está dentro do raio
		if dist <= radius:
			results.append(node.point)

		# Poda da árvore: checar qual caminho seguir
		diff = center[axis] - node.point[axis]
		if diff - radius < 0 and node.left:
			self._radius_query(node.left, center, radius, depth + 1, results)
		if diff + radius >= 0 and node.right:
			self._radius_query(node.right, center, radius, depth + 1, results)

# Depuração e teste
if __name__ == "__main__":
	import pandas as pd
 
	from .config import COORDS_PATH
	from .utils import calcular_limites_retangulo
	
	coords = pd.read_csv(COORDS_PATH)
	tree = KDTree(coords[['latitude', 'longitude']].values.tolist())
	#tree.print()
 
	LAT = -19.922760
	LON = -43.945162
	radius = 3 # km
 
	bounds = calcular_limites_retangulo(LAT, LON, radius)
	print(bounds)
	print(tree.search_rect(bounds[0], bounds[1]))
	