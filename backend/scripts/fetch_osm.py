from pathlib import Path
import time

import pandas as pd
from pandas.errors import EmptyDataError
from geopy.geocoders import Nominatim

PROJECT_ROOT = Path(__file__).parent.parent
ADDRESS_PATH = PROJECT_ROOT / 'data' / 'butecos_bh.csv'
COORDS_PATH = PROJECT_ROOT / 'data' / 'butecos_bh_coords.csv'

HEADER = ["name", "street", "number", "district", "city_state", "zip_code", "latitude", "longitude"]

def load_existing_coords():
    if COORDS_PATH.exists():
        try:
            df = pd.read_csv(COORDS_PATH, dtype=str)
            if df is not None:
                return df[df["latitude"].notna() & df["longitude"].notna()]
        except EmptyDataError:
            pass
    return pd.DataFrame(columns=HEADER)


def build_query_variants(row):
    street = row["street"]
    number = row.get("number", "")
    zip_code = row["zip_code"]
    district = row.get("district", "")
    base = {"city": "Belo Horizonte", "state": "Minas Gerais", "country": "Brazil"}
    no_country = {"city": "Belo Horizonte", "state": "Minas Gerais"}
    return [
        {**base,       "street": f"{street}, {number}", "postalcode": zip_code},  # tudo
        {**no_country, "street": f"{street}, {number}", "postalcode": zip_code},  # sem país
        {**no_country, "street": f"{street}, {number}", "county": district},      # sem CEP, com bairro
        {**no_country, "street": f"{street}, {number}"},                          # só rua + número + cidade/estado
    ]


def struct_osm(name, result):
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


def fetch_missing(df_missing):
    geolocator = Nominatim(user_agent="TP1-ALG2")
    rows = []
    not_found = []
    for _, row in df_missing.iterrows():
        result = None
        matched_query = None
        for query in build_query_variants(row):
            result = geolocator.geocode(query, addressdetails=True, timeout=10)
            time.sleep(1)
            if result:
                matched_query = query
                break
        if result:
            structured = struct_osm(row["name"], result)
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
            not_found.append(row["name"])
            print(f"Coordenada para '{row['name']}' não encontrada.")
        rows.append(structured)
    return pd.DataFrame(rows, columns=HEADER), not_found


def main():
    df_source = pd.read_csv(ADDRESS_PATH, dtype=str)
    df_existing = load_existing_coords()

    already_done = set(df_existing["name"])
    df_missing = df_source[~df_source["name"].isin(already_done)]

    not_found_list = []
    if df_missing.empty:
        print("Todas as coordenadas já foram encontradas.")
    else:
        print(f"Procurando coordenadas de {len(df_missing)} endereços:")
        df_new, not_found_list = fetch_missing(df_missing)
        df_existing = pd.concat([df_existing, df_new], ignore_index=True)

    # Preservar ordem original do arquivo de origem
    df_out = df_source[["name"]].merge(df_existing, on="name", how="left")
    df_out.to_csv(COORDS_PATH, index=False)

    if not_found_list:
        print(f"Endereços não encontrados ({len(not_found_list)}):")
        for address in not_found_list:
            print(address)

if __name__ == "__main__":
    main()
