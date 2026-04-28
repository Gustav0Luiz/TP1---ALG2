## --------- Esse codigo deve gerar um CSV contendo a Latitude e Longitude de cada Bar ------------------ ##


## esta dando errado para alguns endereços

import pandas as pd
import requests
import time

## precisamos extrair o endereço e converter ele em coordenadas
## cada linha do csv eh assim
## <nome do bar> ; <rua>, <numero>,<cidade>,<cep> 

## para cada linha do csv queremos chamar a API OpenStreetMaps e converter
## o endereço em coordenadas geograficas
## a requisição pode ser feita pela seguinte url
#  https://nominatim.openstreetmap.org/search?street=<NUMERO>+<NOME+DA+RUA>&city=<CIDADE>&state=<ESTADO>&postalcode=<CEP>&countrycodes=br&format=jsonv2&limit=1

## primeiro vamos extrair cada bar do csv e adicionar em um dicionario

bares = []
with open('butecos_bh.csv', 'r', encoding='utf-8') as f:
    for linha in f:
        linha = linha.strip() # Remove espaços e o \n do final
        if not linha:
            continue
        #Divide no ';' para separar o Nome do resto do endereço
        dados_bar = linha.split(';', 1)
        nome_bar = dados_bar[0].strip()
        resto_endereco = dados_bar[1].strip()

        # 2. Divide o resto pelas vírgulas
        partes_end = [p.strip() for p in resto_endereco.split(',')]

        # 3. Cria o dicionário com a estrutura desejada
        buteco = {
            "nome": nome_bar,
            "rua": partes_end[0] if len(partes_end) > 0 else "",
            "numero": partes_end[1] if len(partes_end) > 1 else "",
            "cidade": partes_end[2] if len(partes_end) > 2 else "Belo Horizonte",
            "cep": partes_end[3] if len(partes_end) > 3 else ""
        }

        # 4. Adiciona na sua lista principal
        bares.append(buteco)
##a primeira linha (bares[0]) nao contem informações, entao podemos descartar ela.
del bares[0]

### Agora temos uma lista em que cada indice contem um bar, vamos utilizar a API para obter as coordenadas

## ------------- begin aux functions ------------------------------------------------- ##

def fetchAPI(numero, rua, cep):
    base_url = "https://nominatim.openstreetmap.org/search"

    query = f"{rua}, {numero}, Belo Horizonte, MG, {cep}"
    params = {
        'q': query,
        'format': 'jsonv2',
        'limit': 1,
        'countrycodes': 'br'
    }
    
    headers = {'User-Agent': 'TP_ALG2/1.0'}
    
    try:
        response = requests.get(base_url, params=params, headers=headers)
        if response.status_code == 200:
            data = response.json()
            if data:
                return data[0]['lat'], data[0]['lon']
    except Exception as e:
        print(f"Erro na requisição: {e}")
        
    return None, None

## ------------- end aux functions ------------------------------------------------- ##

bars_with_coordinate = []

for bar in bares:
    print(f"Buscando: {bar['nome']}...") 
    lat, lon = fetchAPI(bar["numero"], bar["rua"], bar["cep"])
    
    buteco_complete_data = {
        "nome": bar["nome"], 
        "rua": bar["rua"],
        "numero": bar["numero"],
        "cidade": bar["cidade"],
        "cep": bar["cep"],
        "latitude": lat,
        "longitude": lon
    }
    
    bars_with_coordinate.append(buteco_complete_data)
    
    # para evitar bloqueio, vamos esperar um tempo entre cada req
    time.sleep(0.3)

# ao final nós salvamos os dados em um novo csv
df_resultado = pd.DataFrame(bars_with_coordinate)
df_resultado.to_csv('butecos_com_coordenadas.csv', index=False, sep=',', encoding='utf-8-sig')
