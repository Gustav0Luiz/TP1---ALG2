import pandas as pd
from pandas.errors import EmptyDataError

from ..src.config import ADDRESS_PATH, COORDS_PATH, CSV_HEADER
from ..src.osm import OSMFetcher

def load_existing_coords():
    if COORDS_PATH.exists():
        try:
            df = pd.read_csv(COORDS_PATH, dtype=str)
            if df is not None:
                return df[df["latitude"].notna() & df["longitude"].notna()]
        except EmptyDataError:
            pass
    return pd.DataFrame(columns=CSV_HEADER)

df_source = pd.read_csv(ADDRESS_PATH, dtype=str)
df_existing = load_existing_coords()

already_done = set(df_existing["name"])
df_missing = df_source[~df_source["name"].isin(already_done)]

if df_missing.empty:
    print("Todas as coordenadas já foram encontradas.")
else:
    print(f"Procurando coordenadas de {len(df_missing)} endereços:")
    osm_fetcher = OSMFetcher()
    # df_new = pd.DataFrame([osm_fetcher.fetch(row) for _, row in df_missing.iterrows()])
    df_coords_new = pd.DataFrame([osm_fetcher.fetch(row, coords_only=True) for _, row in df_missing.iterrows()])
    df_existing = pd.concat([df_existing, df_coords_new], ignore_index=True)

df_out = df_source.merge(
    df_existing[["name", "latitude", "longitude"]], 
    on="name", 
    how="left"
)
df_out.to_csv(COORDS_PATH, index=False)