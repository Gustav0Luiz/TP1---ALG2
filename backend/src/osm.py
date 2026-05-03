import time
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter

class OSMFetcher:
    def __init__(self, user_agent: str = "TP1_ALG2"):
        geolocator = Nominatim(user_agent=user_agent, timeout=10)
        self._geocode = RateLimiter(
                            geolocator.geocode,
                            min_delay_seconds=3.0, # 0.33 req/seg (muito conservador)
                            max_retries=2,         # Poucas retentativas
                            error_wait_seconds=10.0 # 10s entre tentativas
                        )
        self._last_request_time = 0

    def _build_query_variants(self, row):
        street = row["street"]
        number = row.get("number", "")
        zip_code = row["zip_code"]
        district = row.get("district", "")
        no_country = {"city": "Belo Horizonte", "state": "Minas Gerais"}
        return [
            {**no_country, "street": f"{street}, {number}", "postalcode": zip_code},
            {**no_country, "street": f"{street}, {number}", "county": district},
            {**no_country, "street": f"{street}, {number}"},
        ]

    def _struct_result(self, name, result):
        address = result.raw.get("address", {})
        return {
            "name": name,
            "street": address.get("road", ""),
            "number": address.get("house_number", ""),
            "district": address.get("suburb") or address.get("neighbourhood", ""),
            "city_state": f"{address.get('city') or address.get('town', '')} - {address.get('state')}",
            "zip_code": address.get("postcode"),
            "latitude": result.raw.get("lat"),
            "longitude": result.raw.get("lon"),
        }

    def fetch(self, row, coords_only=False):
        elapsed = time.time() - self._last_request_time
        if elapsed < 3.5:
            time.sleep(3.5 - elapsed)

        result = None
        matched_query = None
        for query in self._build_query_variants(row):
            result = self._geocode(query, addressdetails=True, timeout=10)
            self._last_request_time = time.time()
            if result:
                matched_query = query
                break
        if result and matched_query:
            structured = self._struct_result(row["name"], result)
            print(f"Coordenada encontrada para '{matched_query['street']}' -> {structured['latitude']}, {structured['longitude']}")
        else:
            structured = {
                "name": row["name"],
                "street": row["street"],
                "number": row.get("number"),
                "district": row.get("district"),
                "city_state": row.get("city_state"),
                "zip_code": row["zip_code"],
                "latitude": None,
                "longitude": None,
            }
            print(f"Coordenada para '{row['name']}' não encontrada.")
        
        coords = (structured["latitude"], structured["longitude"])
        return coords if coords_only else structured