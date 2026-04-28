from pathlib import Path
import csv

from geopy.geocoders import Nominatim
import time

PROJECT_ROOT = Path(__file__).parent.parent
ADDRESS_PATH = PROJECT_ROOT / 'assets' / 'butecos_bh.csv'
COORDS_PATH = PROJECT_ROOT / 'assets' / 'butecos_bh_coords.csv'

def get_addresses():
    with open(ADDRESS_PATH, "r", encoding='utf-8') as infile:
        reader = csv.reader(infile)
        next(reader)  # Skip header
        return [", ".join(row[1:]) for row in reader]

def fetch_osm(addresses):
    geolocator = Nominatim(user_agent="TP1-ALG2")
    results = []
    for address in addresses:
        try:
            result = geolocator.geocode(address, timeout=10)
            results.append(result)
            if result:
                print(f"Geocoded '{address}' -> {result.latitude}, {result.longitude}: {result.address}")
            else:
                print(f"Address '{address}' not found")
        except Exception as e:
            print(f"Failed to geocode '{address}': {e}")
            results.append(None)
        time.sleep(1)  # Nominatim max usage -> 1 req/sec
    return results

with open(COORDS_PATH, "w", encoding='utf-8') as outfile:
    writer = csv.writer(outfile)
    header = ["name", "street", "number", "district", "city_state", "zip_code", "latitude", "longitude"]
    writer.writerow(header)
    results = fetch_osm(get_addresses())
    for i, result in enumerate(results):
        if result:
            address = result.address.split(",")[:-1]
            writer.writerow(address + [result.latitude, result.longitude])
        else:
            writer.writerow([None] * len(header))