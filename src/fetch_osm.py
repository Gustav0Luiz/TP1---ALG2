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
        names = []
        addresses = []
        for row in reader:
            names.append(row[0])
            address = {
                "street": f"{row[1]}, {row[2]}",
                "city": "Belo Horizonte",
                "state": "Minas Gerais",
                "country": "Brazil",
                "postalcode": row[5]
            }
            addresses.append(address)
        return names, addresses
    
def struct_osm(result):
    if not result:
        return None
    address = result.raw.get("address", {})
    return {
        "name": address.get("name", ""),
        "street": address.get("road", ""),
        "number": address.get("house_number", ""),
        "district": address.get('suburb') or address.get('neighbourhood', ''),
        "city_state": f"{address.get('city') or address.get('town', '')} - {address.get('state')}",
        "zip_code": address.get("postcode"),
        "latitude": result.raw.get("lat", ''),
        "longitude": result.raw.get("lon", '')
    }

def fetch_osm(addresses):
    geolocator = Nominatim(user_agent="TP1-ALG2")
    results = []
    for address in addresses:
        result = geolocator.geocode(address, addressdetails=True, timeout=10)
        s_result = struct_osm(result)
        results.append(s_result)
        if s_result:
            print(f"Geocoded '{address}' -> {s_result['latitude']}, {s_result['longitude']}")
        else:
            print(f"Address '{address}' not found")
        time.sleep(0.3)  # Nominatim max usage -> 1 req/sec
    return results

def main():
    names, addresses = get_addresses()
    results = fetch_osm(addresses)

    with open(COORDS_PATH, "w", encoding='utf-8') as outfile:
        writer = csv.writer(outfile)
        header = ["name", "street", "number", "district", "city_state", "zip_code", "latitude", "longitude"]
        writer.writerow(header)
        for name, result in zip(names, results):
            if result:
                writer.writerow([name,
                                 result["street"],
                                 result["number"],
                                 result["district"],
                                 result["city_state"],
                                 result["zip_code"],
                                 result["latitude"],
                                 result["longitude"]]
                                )
            # else:
            #     writer.writerow([name] + [None] * (len(header) - 1))
                
if __name__ == "__main__":
    main()