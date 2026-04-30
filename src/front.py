import csv
import random
import dash_leaflet as dl
import math

from dash import dcc
from dash import Output, Input, State, no_update
from dash_extensions.enrich import DashProxy, html


# objeto principal do seu sistema
app = DashProxy( __name__, assets_folder="../assets")


# Coordenada central inicial
LAT = -19.922760
LON = -43.945162

# Valor inicial usado no mapa
# Neste código, o mesmo input será usado para:
#   - diagonal do retângulo em km
#   - raio do círculo em km
DIAGONAL_KM = 5

# O dl.Circle usa raio em metros
RAIO_METERS = DIAGONAL_KM * 1000


# Ícone personalizado
# A imagem precisa estar na pasta:
# assets/pin.png
custom_icon = {
    "iconUrl": "/assets/pin.png",
    "iconSize": [80, 80],
    "iconAnchor": [40, 80],
    "popupAnchor": [0, -75],
    "tooltipAnchor": [0, -60]
}


def FetchNewAddress(endereco):
    """
    Função temporária.
    Por enquanto gera uma coordenada aleatória em BH.
    Depois você troca pela API real de geocodificação.
    """

    lat_min, lat_max = -19.99, -19.80
    lon_min, lon_max = -44.05, -43.85

    lat = random.uniform(lat_min, lat_max)
    lon = random.uniform(lon_min, lon_max)

    return lat, lon


def ler_mock_file(caminho):
    """
    Lê o arquivo mock_data.csv e cria os marcadores dos bares.

    Considerando o formato:
        últimas 3 colunas:
            linha[-3] = latitude
            linha[-2] = longitude
            linha[-1] = nome do bar

        as colunas anteriores viram o endereço completo.
    """

    markers = []

    try:
        with open(caminho, mode="r", encoding="utf-8") as f:
            leitor = csv.reader(f)

            for linha in leitor:
                if not linha:
                    continue

                try:
                    nome = linha[-1]
                    lat = float(linha[-3])
                    lon = float(linha[-2])

                    endereco_completo = ", ".join(linha[:-3])

                    # IMPORTANTE:
                    # Aqui usamos position=[lat, lon].
                    # Antes estava position=[LAT, LON], o que faria todos os bares
                    # aparecerem no mesmo ponto central.
                    markers.append(
                        dl.Marker(
                            position=[lat, lon],
                            icon=custom_icon,
                            children=[
                                dl.Popup(
                                    html.Div([
                                        html.B(nome, className="popup-title"),
                                        html.Br(),
                                        html.Span(endereco_completo, className="popup-address")
                                    ])
                                ),
                                dl.Tooltip(nome)
                            ]
                        )
                    )

                except ValueError:
                    print(f"Linha ignorada por erro de conversão: {linha}")

    except Exception as e:
        print(f"Erro ao ler arquivo: {e}")

    return markers


def calcular_limites_retangulo(lat_centro, lon_centro, diagonal_km):
    """
    Calcula os bounds do retângulo.

    Como o usuário fornece apenas a diagonal, assumimos que o retângulo será
    um quadrado centralizado no endereço informado.
    """

    # o retangulo eh um quadrado
    lado_km = diagonal_km / math.sqrt(2)  # D = L * raiz(2)
    meio_lado_km = lado_km / 2  # tamanho para cada lado do centro

    # Aproximação:
    # 1 grau de latitude equivale a aproximadamente 111.32 km
    delta_lat = meio_lado_km / 111.32

    # 1 grau de longitude varia conforme a latitude.
    # Fórmula aproximada:
    # km_por_grau_longitude = 111.32 * cos(latitude_em_radianos)
    delta_lon = meio_lado_km / (111.32 * math.cos(math.radians(lat_centro)))

    bounds = [
        [lat_centro - delta_lat, lon_centro - delta_lon],  # canto inferior esquerdo
        [lat_centro + delta_lat, lon_centro + delta_lon]   # canto superior direito
    ]

    return bounds


# Lê os pontos do arquivo mock
meus_pontos = ler_mock_file("mock_data.csv")


# Calcula o retângulo inicial
bounds_retangulo = calcular_limites_retangulo(LAT, LON, DIAGONAL_KM)


# componentes:

# Retângulo inicial da busca
retangulo = dl.Rectangle(
    id="retangulo",
    bounds=bounds_retangulo,
    color="orange",
    weight=2,
    opacity=0.9,
    fillOpacity=0.15
)

# Círculo inicial da busca
circulo = dl.Circle(
    id="circulo",
    center=[LAT, LON],
    radius=RAIO_METERS,
    color="red",
    weight=2,
    opacity=0.9,
    fillOpacity=0.10
)

# Pin central da busca.
# Ele representa o endereço digitado pelo usuário.
pin_centro = dl.Marker(
    id="pin-centro",
    position=[LAT, LON],
    icon=custom_icon,
    children=[
        dl.Popup("Centro da busca"),
        dl.Tooltip("Centro da busca")
    ]
)


app.layout = html.Div([

    ## data cached
    # dcc.Store guarda dados no navegador.
    # Aqui vamos guardar a última latitude, longitude, endereço e raio/diagonal usados.
    dcc.Store(
        id="cache-localizacao",
        data={
            "lat": LAT,
            "lon": LON,
            "endereco": None,
            "raio": DIAGONAL_KM
        }
    ),

    html.H2(
        "Explorador Comida Di Buteco 2026 - BH",
        className="titulo"
    ),

    html.Div([

        html.Div([
            dcc.Input(
                id="barra-busca",
                type="text",
                placeholder="🔍︎ Insira seu endereço",
                persistence=True,
                className="input-busca"
            )
        ], className="container-input-busca"),

        html.Div([

            html.Label(
                "Raio / Diagonal (km):",
                className="label-raio"
            ),

            dcc.Input(
                id="input-alcance",
                type="number",
                value=DIAGONAL_KM,
                min=0.1,
                step=0.1,
                className="input-raio"
            )

        ], className="container-raio"),

        html.Button(
            "Buscar",
            id="botao-buscar",
            n_clicks=0,
            title="Buscar endereço ou atualizar raio",
            className="botao-buscar"
        )

    ], className="container-controles"),

    html.Div([

        dl.Map(
            [
                # dl.TileLayer é o fundo do mapa
                dl.TileLayer(),

                dl.FullScreenControl(),

                # Pin central da busca
                pin_centro,

                # Retângulo calculado a partir da diagonal
                retangulo,

                # Círculo calculado a partir do raio
                circulo,

                ## camada de pontos
                # Aqui ficam os bares lidos do mock_data.csv
                dl.LayerGroup(
                    id="camada-pontos",
                    children=meus_pontos
                )

            ],
            id="mapa-principal",
            center=[LAT, LON],
            zoom=16,
            className="mapa"
        )

    ], className="container-mapa"),

    html.Div(
        id="tabela-resultados",
        className="container-tabela"
    )

], className="pagina")


@app.callback(
    Output("mapa-principal", "viewport"),
    Output("cache-localizacao", "data"),
    Output("retangulo", "bounds"),
    Output("circulo", "center"),
    Output("circulo", "radius"),
    Output("pin-centro", "position"),

    Input("botao-buscar", "n_clicks"),

    State("barra-busca", "value"),
    State("input-alcance", "value"),
    State("cache-localizacao", "data"),

    prevent_initial_call=True
)
def buscar_ou_atualizar(n_clicks, endereco_digitado, raio_digitado, cache_atual):

    # Se por algum motivo o cache estiver vazio, recriamos com os valores iniciais.
    if cache_atual is None:
        cache_atual = {
            "lat": LAT,
            "lon": LON,
            "endereco": None,
            "raio": DIAGONAL_KM
        }

    # Se o usuário não digitar raio/diagonal, usa o valor do cache.
    if raio_digitado is None:
        raio_digitado = cache_atual.get("raio", DIAGONAL_KM)

    # Remove espaços extras do endereço digitado.
    if endereco_digitado is not None:
        endereco_digitado = endereco_digitado.strip()

    endereco_cache = cache_atual.get("endereco")
    raio_cache = cache_atual.get("raio")

    # Verifica se o usuário mudou o endereço ou apenas mudou o raio/diagonal.
    endereco_mudou = bool(endereco_digitado) and endereco_digitado != endereco_cache
    raio_mudou = raio_digitado != raio_cache

    # Se nada mudou, não atualiza nada na tela.
    if not endereco_mudou and not raio_mudou:
        return no_update, no_update, no_update, no_update, no_update, no_update

    # Se o endereço mudou, busca uma nova coordenada.
    # Por enquanto FetchNewAddress gera uma coordenada aleatória em BH.
    if endereco_mudou:
        lat, lon = FetchNewAddress(endereco_digitado)
    else:
        # Se só o raio/diagonal mudou, mantém o centro anterior.
        lat = cache_atual.get("lat")
        lon = cache_atual.get("lon")

    nova_posicao = [lat, lon]

    # viewport com transition="flyTo" faz o efeito nativo de voar até o ponto.
    viewport = {
        "center": nova_posicao,
        "zoom": 16,
        "transition": "flyTo"
    }

    # Atualiza o retângulo com base na nova posição e na nova diagonal.
    novo_bounds = calcular_limites_retangulo(lat, lon, raio_digitado)

    # Atualiza o círculo.
    # O input está em km, mas o dl.Circle usa metros.
    novo_raio_metros = raio_digitado * 1000

    # Atualiza o cache com os últimos valores usados.
    novo_cache = {
        "lat": lat,
        "lon": lon,
        "endereco": endereco_digitado if endereco_mudou else endereco_cache,
        "raio": raio_digitado
    }

    # A ordem do return precisa ser a mesma ordem dos Outputs.
    return (
        viewport,           # Output("mapa-principal", "viewport")
        novo_cache,         # Output("cache-localizacao", "data")
        novo_bounds,        # Output("retangulo", "bounds")
        nova_posicao,       # Output("circulo", "center")
        novo_raio_metros,   # Output("circulo", "radius")
        nova_posicao        # Output("pin-centro", "position")
    )


if __name__ == "__main__":
    app.run(debug=True)