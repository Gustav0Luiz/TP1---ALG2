from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent
ADDRESS_PATH = PROJECT_ROOT / 'data' / 'butecos_bh.csv'
COORDS_PATH = PROJECT_ROOT / 'data' / 'butecos_bh_coords.csv'

CSV_HEADER = ["name", "street", "number", "district", "city_state", "zip_code", "latitude", "longitude"]