"""
components/map_components.py

Responsabilidade do arquivo:
- Centralizar os componentes visuais relacionados ao mapa.
- Criar camadas fixas/controláveis do dash-leaflet.
- Definir botões do mapa, como:
    - botão para ligar/desligar a divisão dos bairros;
    - botão para alternar entre mapa padrão e mapa satélite.
- Definir camadas que serão atualizadas por callbacks no main.py.

Esses objetos são importados no main.py e usados dentro do dl.Map.
"""

import dash_leaflet as dl
from frontend.utils.config import LAT, LON, custom_icon_search_pin

# Área de busca exibida no mapa.
# Inicialmente começa vazia.
# Depois, o callback no main.py altera o children para exibir:
# - um retângulo; ou
# - um círculo.
area_busca = dl.LayerGroup(
    id="area-busca",
    children=[]
)


# Pin central da busca.
# Ele representa o endereço digitado pelo usuário.
# A posição inicial está na Praça Raul Soares.
camada_pin_centro = dl.LayerGroup(
    id="camada-pin-centro",
    children=[]
)

# GeoJSON com a divisão dos bairros de Belo Horizonte.
# O arquivo bairros_bh.geojson deve estar dentro da pasta assets.
# Este componente desenha apenas o contorno dos bairros.
bairros = dl.GeoJSON(
    url="/assets/bairros_bh.geojson",
    id="bairros-bh",
    options={
        "style": {
            "color": "#2C3E50", # Azul petróleo profundo
            "weight": 0.8, # Linha ultra fina
            "opacity": 0.5,
            "fillOpacity": 0.05, # Um leve "véu" para distinguir as áreas
            "fillColor": "#BDC3C7" 
        }
    }
)


# Botão para ligar/desligar a visualização da divisão dos bairros.
# O callback no main.py usa o id "btn-bairros".
bairro_btn = dl.EasyButton(
    icon="""
        <img 
            class="icone-bairros"
            src="/assets/bairro_icon.png"
        >
    """,
    title="Mostrar/ocultar bairros",
    id="btn-bairros"
)


# Camada controlável dos bairros.
# Em vez de remover diretamente o componente bairros,
# o callback altera o children desta camada:
# - children=[bairros] mostra os bairros;
# - children=[] esconde os bairros.
camada_bairros = dl.LayerGroup(
    id="camada-bairros",
    children=[bairros]
)


# TileLayer padrão do mapa.
# Atualmente usa o estilo Voyager da CartoDB.
tile_mapa_padrao = dl.TileLayer(
    url="https://{s}.basemaps.cartocdn.com/rastertiles/voyager/{z}/{x}/{y}{r}.png",
    attribution="© OpenStreetMap © CARTO"
)


# TileLayer de satélite.
# Atualmente usa o Alidade Satellite da Stadia Maps.
tile_satelite = dl.TileLayer(
    url="https://tiles.stadiamaps.com/tiles/alidade_satellite/{z}/{x}/{y}{r}.jpg",
    attribution="© Stadia Maps © OpenMapTiles © OpenStreetMap"
)


# Camada controlável do mapa base.
# O callback no main.py alterna o children entre:
# - [tile_mapa_padrao]
# - [tile_satelite]
camada_mapa_base = dl.LayerGroup(
    id="camada-mapa-base",
    children=[tile_mapa_padrao]
)


# Botão para alternar entre o mapa padrão e o mapa satélite.
# O callback no main.py usa o id "btn-satelite".
satelite_btn = dl.EasyButton(
    icon="""
        <img 
            class="icone-controle-mapa"
            src="/assets/layer_icon.png"
        >
    """,
    title="Alternar mapa/satélite",
    id="btn-satelite"
)