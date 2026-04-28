## Esse codigo deve pegar a requisição do usuario no front end e obter a Lat e Lon

### ainda esta com bugs, so comecei

import requests
### O usuario vai digitar o endereço dele na barra de busca
### A partir disso temos que obter lat e lon.

# exemplo: usuario digita "Rua dos tupis, 1534"
## precisamos obter a lat/lon para gerar o mapa centralizado nesse endereço.


def getLatLon(rua, numero, bairro):
    base_url = "https://nominatim.openstreetmap.org/search"
    
    params = {
        'street': f"{numero} {rua}",
        'neighborhood': bairro, 
        'city': 'Belo Horizonte',
        'state': 'Minas Gerais',
        'countrycodes': 'br',
        'format': 'jsonv2',
        'limit': 1
    }
    
    headers = {'User-Agent': 'TP_ALG2_Gustavo/1.0'}
    
    try:
        response = requests.get(base_url, params=params, headers=headers)
        if response.status_code == 200:
            data = response.json()
            if data:

                return data[0]['lat'], data[0]['lon'], data[0]['display_name']
    except Exception as e:
        print(f"Erro na requisição: {e}")
    return None, None, None

entrada = input("Digite o endereço (Rua, Numero, Bairro): ")

try:
    partes = [p.strip() for p in entrada.split(",")]
    
    if len(partes) == 3:
        rua, numero, bairro = partes
        lat, lon, endereco_completo = getLatLon(rua, numero, bairro)

        if lat and lon:
            print("\n--- Localização Encontrada ---")
            print(f"Busca: Rua {rua}, {numero} - {bairro}")
            print(f"Retorno oficial: {endereco_completo}")
            print(f"Latitude: {lat}")
            print(f"Longitude: {lon}")
        else:
            print("\n[!] Endereço não encontrado. Verifique se o nome da rua ou bairro estão corretos.")
    else:
        print("\n[!] Erro: Você deve digitar os três itens separados por vírgula (Rua, Numero, Bairro).")

except Exception as e:
    print(f"\n[!] Ocorreu um erro inesperado: {e}")

