#### Tutorial da biblioteca que temos que utilizar

# Dash layout: html.Div, dcc.Input, html.Button, dash_table.DataTable.
# Dash callbacks: atualizar mapa e tabela quando o usuário buscar.
# dash-leaflet básico: dl.Map, dl.TileLayer, dl.Marker, dl.Popup, dl.Rectangle.
# CSS em Dash: criar pasta assets/style.css e estilizar tudo por className.
# Leaflet conceitual: entender marker, popup, tile layer, bounds, rectangle e circle.

import dash_leaflet as dl
from dash_extensions.enrich import DashProxy
import math
from dash import Dash, html, dcc, Input, Output, State

# objeto principal do seu sistema
app = DashProxy()

# app.layout define o que aparece na tela.
# dentro do objeto layout podemos passar:

#       Elementos HTML -   representa elementos HTML comuns da página.

#       DCC - O dcc significa Dash Core Components.
#           componentes interativos mais avançados, como campos de entrada, dropdowns, sliders e gráficos.

#       DL - O dl vem do dash-leaflet. Serve para criar e controlar o mapa.
#           tudo relacionado ao mapa: fundo, pinos, popups, retângulos e círculos.

#       Dash-tabel - O dash_table serve para criar tabelas interativas.
#               tabela de resultados abaixo do mapa.

### retangulo:
#   bounds = [
#       [latitude_canto_inferior_esquerdo, longitude_canto_inferior_esquerdo],
#       [latitude_canto_superior_direito, longitude_canto_superior_direito]
#   ]

## calculo do retangulo
def calcular_limites_retangulo(lat_centro, lon_centro, diagonal_km):
    # o retangulo eh um quadrado
    lado_km = diagonal_km / math.sqrt(2)  # (D = L * raiz(2))
    meio_lado_km = lado_km / 2 # tamanho para cada lado do centro

    # Aproximação:
    # 1 grau de latitude equivale a aproximadamente 111km
    delta_lat = meio_lado_km / 111

    # 1 grau de longitude varia conforme a latitude - vide formula:
    # 1 km =  111.32 * cos(latitude_em_radianos)
    delta_lon = meio_lado_km / (111.32 * math.cos(math.radians(lat_centro)))

    bounds = [
        [lat_centro - delta_lat, lon_centro - delta_lon],  # canto inferior esquerdo
        [lat_centro + delta_lat, lon_centro + delta_lon]   # canto superior direito
    ]
    return bounds


# Coordenada central
LAT = -19.922760
LON = -43.945162
DIAGONAL_KM = 5
RAIO_METERS = 4000

bounds_retangulo = calcular_limites_retangulo(LAT, LON, DIAGONAL_KM)


# Ícone personalizado
custom_icon = {
    "iconUrl": "/assets/pin.png",
    "iconSize": [80, 80],
    "iconAnchor": [40, 80],
    "popupAnchor": [0, -75],
    "tooltipAnchor": [0, -60]
}


# componentes:

marcadores = dl.Marker(id = "pin", position=[LAT, LON],icon=custom_icon,children=[dl.Popup("Bar teste"),dl.Tooltip("Bar teste")])
retangulo = dl.Rectangle(id="retangulo",bounds=bounds_retangulo, color="orange", weight=2,opacity=0.9)           
circulo = dl.Circle(id="circulo",center=[LAT,LON],radius=RAIO_METERS,color="red", weight=2,opacity=0.9)            
            
                
                


app.layout = html.Div([

    # input
    html.Div([
        dcc.Input(
            id="input-lat",
            type="number",
            value=LAT,
            step=0.000001,
            placeholder="Latitude"
        ),

        dcc.Input(
            id="input-lon",
            type="number",
            value=LON,
            step=0.000001,
            placeholder="Longitude"
        ),

        html.Button("Ir", id="btn-ir", n_clicks=0)
    ]),


    # mapa
    dl.Map(
        id="mapa",
        center=[LAT, LON],
        zoom=16,
        style={"height": "80vh", "width": "100%"},
        attributionControl=False,
        children=[
            dl.TileLayer(),
            dl.FullScreenControl(),
            marcadores,
            retangulo,
            circulo
        ]
    )
])


@app.callback(
    Output("mapa", "viewport"), # Atualiza a propriedade viewport do componente com id "mapa".
    Output("pin", "position"), # Atualiza a propriedade position do componente com id "pin".
    Output("retangulo", "bounds"), # atualiza a diagonal
    Output("circulo", "center"),  # atualiza o raio
    Input("btn-ir", "n_clicks"), # Execute a função quando o btn-ir for clicado. O n_clicks guarda quantas vezes o botão foi clicado.
    State("input-lat", "value"), # Lê o valor digitado no input de latitude.
    State("input-lon", "value"), # Lê o valor digitado no input de longitude.
    prevent_initial_call=True
)

def fly_to_local(n_clicks, lat, lon):
    nova_posicao = [lat, lon]

    viewport = {
        "center": nova_posicao,
        "zoom": 16,
        "transition": "flyTo"
    }

    novo_bounds = calcular_limites_retangulo(lat, lon, DIAGONAL_KM)

    return viewport, nova_posicao, novo_bounds, nova_posicao






if __name__ == "__main__":
    app.run(debug=True)