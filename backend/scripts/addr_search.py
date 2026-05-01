import json
import csv
from pathlib import Path
from collections import defaultdict

import sys
sys.path.append(str(Path(__file__).parent.parent))

from src.config import COORDS_PATH, SEARCH_CACHE_PATH
from src.kdtree import KDTree
from src.osm import OSMFetcher
from src.utils import calcular_distancia_km, calcular_limites_retangulo, estimar_raio_graus

class AddressSearcher:
	def __init__(self, coords_path: Path = COORDS_PATH, cache_path: Path = SEARCH_CACHE_PATH):
		self.coords_path = Path(coords_path)
		self.cache_path = Path(cache_path)
		self.osm_fetcher = OSMFetcher()

		self._geocode_cache = self._load_geocode_cache()
		self._records = self._load_records()
		self._coord_index = self._build_coord_index(self._records)
		self._tree = self._build_kdtree(self._coord_index)

    # ______________ CACHE ______________
    
	def _load_geocode_cache(self) -> dict:
		if not self.cache_path.exists():
			return {}
		try:
			with open(self.cache_path, "r", encoding="utf-8") as f:
				data = json.load(f)
				return data.get("geocode", {})
		except (json.JSONDecodeError, OSError):
			return {}

	def _save_geocode_cache(self) -> None:
		with open(self.cache_path, "w", encoding="utf-8") as f:
			json.dump({"geocode": self._geocode_cache}, f, ensure_ascii=False, indent=2)


	# _________ CARREGAMENTO E INDEXAÇÃO DOS DADOS _________
 
	def _load_records(self) -> list[dict]:
		records = []
		with open(self.coords_path, "r", encoding="utf-8") as f:
			reader = csv.DictReader(f)
			for row in reader:
				parsed_row = self._parse_coordinate_row(row)
				if parsed_row:
					records.append(parsed_row)
		return records

	def _parse_coordinate_row(self, row: dict) -> dict | None:
		if not row.get("latitude") or not row.get("longitude"):
			return None
		try:
			row["latitude"] = float(row["latitude"])
			row["longitude"] = float(row["longitude"])
			return row
		except ValueError:
			return None

	def _build_coord_index(self, records: list[dict]) -> dict:
        # defaultdict para facilitar a inserção de novos índices (cria automaticamente)
		index = defaultdict(list)
		for record in records:
			coord = (record["latitude"], record["longitude"])
			index[coord].append(record)
		return dict(index)

	def _build_kdtree(self, coord_index: dict) -> KDTree:
		unique_coords = [list(coord) for coord in coord_index.keys()]
		return KDTree(unique_coords)

	# ______________ OSM ______________
 
	def _get_center_coords(self, address: str) -> tuple[float, float]:
		cache_key = address.strip().lower()
		
		if cache_key in self._geocode_cache:
			return tuple(self._geocode_cache[cache_key])

		coords_tuple = self._fetch_from_osm(address)
		
		self._geocode_cache[cache_key] = coords_tuple
		self._save_geocode_cache()
		
		return coords_tuple

	def _fetch_from_osm(self, address: str) -> tuple[float, float]:
		query_row = {
			"name": address.strip(),
			"street": address.strip(),
			"number": "",
			"district": "",
			"zip_code": ""
		}
		
		coords = self.osm_fetcher.fetch(query_row, coords_only=True)
		if not coords or None in coords:
			raise ValueError(f"Address not found: {address}")

		return float(coords[0]), float(coords[1])

	# ______________ KDTREE ______________
	def _get_candidates(self, center_coords: tuple, distance_km: float, use_circle: bool) -> set[tuple]:
		if use_circle:
			radius_deg = estimar_raio_graus(center_coords[0], distance_km)
			points = self._tree.search_radius(center_coords, radius_deg)
		else:
			point_min, point_max = calcular_limites_retangulo(*center_coords, distance_km)
			points = self._tree.search_rect(point_min, point_max)

		return {tuple(p) for p in points}

	def _format_results(self, candidate_coords: set[tuple], center_coords: tuple):#, distance_km: float, use_circle: bool) -> list[dict]:
		results = []

		for coord in candidate_coords:
			dist = calcular_distancia_km(center_coords, coord)

			# # Filter out points beyond the radius if circular search is enabled
			# if use_circle and dist > distance_km:
			# 	continue

			# Listar os dados
			for record in self._coord_index.get(coord, []):
				result_item = dict(record)
				result_item["distance_km"] = dist
				results.append(result_item)
        
        # Retornar ordenado por distância
		return sorted(results, key=lambda x: (x["distance_km"], x.get("name", "")))

	# ______________ METODO PRINCIPAL ______________
 
	def search_addresses(self, center_address: str, distance_km: float, use_circle: bool = False) -> list[dict]:
		if not center_address or not center_address.strip():
			raise ValueError("center_address cannot be empty")
		if distance_km is None or distance_km <= 0:
			raise ValueError("distance_km must be greater than zero")

		center_coords = self._get_center_coords(center_address)
		candidate_coords = self._get_candidates(center_coords, distance_km, use_circle)

		## modificado para retornar a coordenada central, para nao ter que calcular novamente no front
		results = self._format_results(candidate_coords, center_coords)

		return {"center": center_coords,"results": results}
				
				
			

if __name__ == "__main__":
    searcher = AddressSearcher()

    test_address = "Praça da Liberdade"
    test_distance = 2.0  # km

    rect_response = searcher.search_addresses(
        center_address=test_address,
        distance_km=test_distance,
        use_circle=False
    )

    rect_center = rect_response["center"]
    rect_results = rect_response["results"]

    print("Rect search:")
    print(f"Center: {rect_center}")

    for rect in rect_results:
        print(rect["name"], f"{rect['distance_km']:.2f}km", sep=": ")

    circle_response = searcher.search_addresses(
        center_address=test_address,
        distance_km=test_distance,
        use_circle=True
    )

    circle_center = circle_response["center"]
    circle_results = circle_response["results"]

    print("\nCircle search:")
    print(f"Center: {circle_center}")

    for circle in circle_results:
        print(circle["name"], f"{circle['distance_km']:.2f}km", sep=": ")