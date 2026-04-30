import csv
import random
import dash_leaflet as dl

from dash import dcc
from dash import Output, Input, State, no_update
from dash_extensions.enrich import DashProxy, html


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

    print(f"Fetch executado para o endereço: {endereco}")
    print(f"Nova coordenada: {lat}, {lon}")

    return lat, lon


def ler_mock_file(caminho):
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

                    markers.append(
                        dl.Marker(
                            position=[lat, lon],
                            children=[
                                dl.Popup(
                                    html.Div([
                                        html.B(nome, className="popup-title"),
                                        html.Br(),
                                        html.Span(endereco_completo, className="popup-address")
                                    ])
                                )
                            ]
                        )
                    )

                except ValueError:
                    print(f"Linha ignorada por erro de conversão: {linha}")

    except Exception as e:
        print(f"Erro ao ler arquivo: {e}")

    return markers


app = DashProxy()

meus_pontos = ler_mock_file("mock_data.csv")

centro_inicial = [-19.869449, -43.964535]


app.layout = html.Div([

    dcc.Store(
        id="cache-localizacao",
        data={
            "lat": centro_inicial[0],
            "lon": centro_inicial[1],
            "endereco": None,
            "raio": 2.0
        }
    ),

    html.H2(
        "Explorador Comida Di Buteco 2026 – BH",
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
                "Raio (km):",
                className="label-raio"
            ),

            dcc.Input(
                id="input-alcance",
                type="number",
                value=2.0,
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

        dl.Map([

            dl.TileLayer(),

            dl.LayerGroup(
                id="camada-pontos",
                children=meus_pontos
            )

        ],
            id="mapa-principal",
            center=centro_inicial,
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
    Input("botao-buscar", "n_clicks"),
    State("barra-busca", "value"),
    State("input-alcance", "value"),
    State("cache-localizacao", "data"),
    prevent_initial_call=True
)
def buscar_ou_atualizar(n_clicks, endereco_digitado, raio_digitado, cache_atual):

    if cache_atual is None:
        cache_atual = {
            "lat": centro_inicial[0],
            "lon": centro_inicial[1],
            "endereco": None,
            "raio": 2.0
        }

    if raio_digitado is None:
        raio_digitado = cache_atual.get("raio", 2.0)

    if endereco_digitado is not None:
        endereco_digitado = endereco_digitado.strip()

    endereco_cache = cache_atual.get("endereco")
    raio_cache = cache_atual.get("raio")

    endereco_mudou = bool(endereco_digitado) and endereco_digitado != endereco_cache
    raio_mudou = raio_digitado != raio_cache

    if not endereco_mudou and not raio_mudou:
        return no_update, no_update

    if endereco_mudou:
        lat, lon = FetchNewAddress(endereco_digitado)

        viewport = {
            "center": [lat, lon],
            "zoom": 16,
            "transition": "flyTo"
        }

        novo_cache = {
            "lat": lat,
            "lon": lon,
            "endereco": endereco_digitado,
            "raio": raio_digitado
        }

        return viewport, novo_cache

    novo_cache = {
        "lat": cache_atual.get("lat"),
        "lon": cache_atual.get("lon"),
        "endereco": endereco_cache,
        "raio": raio_digitado
    }

    return no_update, novo_cache


if __name__ == "__main__":
    app.run(debug=True)