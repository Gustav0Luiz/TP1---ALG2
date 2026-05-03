# ---------------------- IMPORTS ----------------------

import dash_leaflet as dl

from dash import dcc, Input, Output, State, no_update, ctx
from dash_extensions.enrich import DashProxy, html
from frontend.utils.config import LAT, LON, custom_icon_bar_pin, custom_icon_search_pin
from frontend.utils.geo import calcular_limites_retangulo
from frontend.utils.table_components import CreateTableDataFromResults, create_tabela_resultados

from backend.scripts.addr_search import AddressSearcher

from frontend.components.map_components import (
    area_busca,
    camada_pin_centro,
    bairros,
    bairro_btn,
    camada_bairros,
    tile_mapa_padrao,
    tile_satelite,
    camada_mapa_base,
    satelite_btn
)


# ---------------------- ORQUESTRADOR ----------------------

# O AddressSearcher carrega:
# - dados dos bares geocodificados;
# - cache de endereços;
# - k-d tree;
# - métodos de busca por retângulo/círculo.
searcher = AddressSearcher()


# ---------------------- FUNÇÕES AUXILIARES DO MAIN ----------------------

def CreateMarkers(bares):
    """
    Cria os marcadores do mapa a partir de uma lista de bares.
    """

    if bares is None:
        bares = []

    markers = []

    for i, bar in enumerate(bares):
        endereco = f"{bar.get('street', '')}"

        if bar.get("number"):
            endereco += f", {bar['number']}"

        endereco += f" - {bar.get('district', '')}, {bar.get('city_state', '')}"

        marker = dl.Marker(
            id={
                "type": "bar-marker",
                "index": f"{bar.get('name', '')}-{i}"
            },
            position=[float(bar["latitude"]), float(bar["longitude"])],
            icon=custom_icon_bar_pin,
            children=[
                dl.Popup(
                    html.Div([
                        html.Div(
                            bar.get("name", ""),
                            className="popup-title"
                        ),

                        html.Div(
                            endereco,
                            className="popup-address"
                        ),

                        html.Div(
                            bar.get("zip_code", ""),
                            className="popup-cep"
                        )
                    ], className="popup-card")
                ),
            ]
        )

        markers.append(marker)


    return markers


def SearchTreeAndGetPoints(bares=None):
    """
    Cria a camada inicial de pontos do mapa.

    Se nenhum conjunto de bares for enviado, exibe todos os bares carregados
    pelo orquestrador.
    """

    if bares is None:
        bares = searcher._records

    return dl.LayerGroup(
        id="camada-pontos",
        children=CreateMarkers(bares)
    )


# ---------------------- DADOS E COMPONENTES INICIAIS ----------------------

# Inicialmente o mapa exibe todos os bares disponíveis.
meus_pontos = SearchTreeAndGetPoints()

# A tabela começa vazia.
tabela_resultados = create_tabela_resultados([])


# ---------------------- APP ----------------------

app = DashProxy(
    __name__,
    assets_folder="assets"
)

# nome do site
app.title = "Explorador Comida Di Buteco BH"

# ---------------------- LAYOUT ----------------------

app.layout = html.Div([

    html.Div([
        html.Div([
            html.Span(className="risco risco-1"),
            html.Span(className="risco risco-2"),
            html.Span(className="risco risco-3"),
        ], className="efeito-titulo efeito-esquerda"),

        html.H2(
            "Explorador Comida Di Buteco 2026 - BH",
            className="titulo"
        ),

        html.Div([
            html.Span(className="risco risco-1"),
            html.Span(className="risco risco-2"),
            html.Span(className="risco risco-3"),
        ], className="efeito-titulo efeito-direita"),
    ], className="container-titulo"),

    html.P(
    "Busque bares próximos a um endereço e visualize os resultados no mapa.",
    className="subtitulo"
    ),

    html.Div([

        html.Div([
            dcc.Input(
                id="barra-busca",
                type="text",
                placeholder="🔍︎ Insira seu endereço",
                persistence=False,
                className="input-busca"
            )
        ], className="container-input-busca"),

        html.Div([
            html.Label(
                "Alcance da Busca (km):",
                className="label-raio"
            ),

            dcc.Input(
                id="input-alcance",
                type="number",
                placeholder="Alcance",
                min=0.1,
                step=0.01,
                className="input-raio"
            )
        ], className="container-raio"),

        html.Button(
            "Buscar",
            id="botao-buscar",
            n_clicks=0,
            title="Buscar endereço",
            className="botao-buscar"
        ),

        html.Button(
            "Limpar",
            id="botao-limpar",
            n_clicks=0,
            title="Limpar área de busca",
            className="botao-limpar"
        ),

        html.Div([
            dcc.RadioItems(
                id="tipo-busca",
                options=[
                    {
                        "label": html.Span([
                            "Retângulo",
                            html.Span(
                                "Calculado a partir da diagonal do retângulo.",
                                className="tooltip-opcao"
                            )
                        ], className="opcao-toggle-com-tooltip"),
                        "value": "retangulo"
                    },
                    {
                        "label": html.Span([
                            "Círculo",
                            html.Span(
                                "Calculado a partir do raio do círculo.",
                                className="tooltip-opcao"
                            )
                        ], className="opcao-toggle-com-tooltip"),
                        "value": "circulo"
                    }
                ],
                value="retangulo",
                className="toggle-slider"
            )
        ], className="container-toggle")

    ], className="container-controles"),

    html.Div(
    id="mensagem-busca",
    className="mensagem-busca"
    ),

    html.Div([

        dl.Map([

            # Camada do mapa base.
            # O callback alterna entre mapa normal e satélite.
            camada_mapa_base,

            # Permite modo tela cheia.
            dl.FullScreenControl(),

            # Botão ligar/desligar divisão dos bairros.
            bairro_btn,

            # Botão alternar mapa/satélite.
            satelite_btn,

            # Camada controlável dos bairros.
            camada_bairros,

            # Pin central da busca.
            camada_pin_centro,

            # Área de busca: começa vazia e depois recebe retângulo ou círculo.
            area_busca,

            # Camada de pontos dos bares.
            meus_pontos

        ],
            id="mapa-principal",
            center=[LAT, LON],
            zoom=15,
            className="mapa",
            attributionControl=False
        )

    ], className="container-mapa"),

    html.Div([
        html.H3("Bares encontrados", className="titulo-tabela"),
        tabela_resultados
    ], className="container-tabela")

], className="pagina")


# ---------------------- CALLBACK: BUSCAR / LIMPAR ----------------------

@app.callback(
    Output("mapa-principal", "viewport"),
    Output("area-busca", "children"),
    Output("camada-pin-centro", "children"),
    Output("tabela-bares", "data"),
    Output("camada-pontos", "children"),
    Output("mensagem-busca", "children"),

    Input("botao-buscar", "n_clicks"),
    Input("botao-limpar", "n_clicks"),

    State("barra-busca", "value"),
    State("input-alcance", "value"),
    State("tipo-busca", "value"),

    prevent_initial_call=True
)
def buscar_ou_limpar(
    n_clicks_buscar,
    n_clicks_limpar,
    endereco_digitado,
    alcance_digitado,
    tipo_busca
):
    """
    Executado quando o usuário clica em Buscar ou Limpar.

    Buscar:
    - chama o orquestrador;
    - recebe centro e bares filtrados;
    - desenha retângulo/círculo;
    - atualiza tabela;
    - atualiza pins.

    Limpar:
    - remove área de busca;
    - volta a exibir todos os bares;
    - esvazia a tabela.
    """

    acao = ctx.triggered_id

    # ----------------------
    # LIMPAR BUSCA
    # ----------------------
    if acao == "botao-limpar":
        todos_bares = searcher._records
        todos_markers = CreateMarkers(todos_bares)

        return (
            no_update,      # mantém o mapa na posição atual
            [],             # remove retângulo/círculo
            [],             # remove o pin central
            [],             # tabela vazia
            todos_markers,   # volta a exibir todos os bares
            "",             # mensagem de busca
        )

    # ----------------------
    # BUSCAR ENDEREÇO
    # ----------------------
    if endereco_digitado is None or endereco_digitado.strip() == "":
        return no_update, no_update, no_update, no_update, no_update, "Digite um endereço para realizar a busca."

    if alcance_digitado is None:
        return no_update, no_update, no_update, no_update, no_update, "Digite um valor de alcance para realizar a busca."

    try:
        alcance_digitado = float(alcance_digitado)
    except (TypeError, ValueError):
        return no_update, no_update, no_update, no_update, no_update, "O alcance deve ser um número maior que zero."

    if alcance_digitado <= 0:
       return no_update, no_update, no_update, no_update, no_update, "O alcance deve ser maior que zero."

    if tipo_busca is None:
        tipo_busca = "retangulo"

    endereco_digitado = endereco_digitado.strip()

    use_circle = tipo_busca == "circulo"

    try:
        resposta = searcher.search_addresses(
            center_address=endereco_digitado,
            distance_km=alcance_digitado,
            use_circle=use_circle
        )
    except Exception as e:
        return no_update, no_update, no_update, no_update, no_update, "Erro ao buscar endereço. Tente outro endereço ou tente mais tarde."
    
    if resposta is None or resposta.get("center") is None:
        return (
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            "Endereço não encontrado. Tente informar rua, número e bairro. "
        )

    lat, lon = resposta["center"]
    lat = float(lat)
    lon = float(lon)

    bares_filtrados = resposta["results"]
    nova_posicao = [lat, lon]
    novo_pin_centro = [
        dl.Marker(
            id="pin-centro",
            position=nova_posicao,
            icon=custom_icon_search_pin
        )
    ]

    novos_dados_tabela = CreateTableDataFromResults(bares_filtrados)
    novos_markers = CreateMarkers(bares_filtrados)

    viewport = {
        "center": nova_posicao,
        "zoom": 15,
        "transition": "flyTo"
    }

    if tipo_busca == "retangulo":
        novo_bounds = calcular_limites_retangulo(
            lat,
            lon,
            alcance_digitado
        )

        nova_area_busca = [
            dl.Rectangle(
                bounds=novo_bounds,
                color="#F27405",
                fillColor="#FFB948",
                weight=2,
                opacity=0.8,
                fillOpacity=0.15
            )
        ]

    else:
        raio_metros = alcance_digitado * 1000

        nova_area_busca = [
            dl.Circle(
                center=nova_posicao,
                radius=raio_metros,
                color="#F27405",
                fillColor="#FFB948",
                weight=2,
                opacity=0.8,
                fillOpacity=0.15
            )
        ]

    return (
            viewport,
            nova_area_busca,
            novo_pin_centro,
            novos_dados_tabela,
            novos_markers,
            ""
    )


# ---------------------- CALLBACK: MOSTRAR/OCULTAR BAIRROS ----------------------

@app.callback(
    Output("camada-bairros", "children"),
    Input("btn-bairros", "n_clicks"),
    prevent_initial_call=True
)
def alternar_bairros(n_clicks):
    """
    Liga/desliga a visualização da divisão dos bairros.
    """

    # Clique ímpar: esconde bairros
    if n_clicks % 2 == 1:
        return []

    # Clique par: mostra bairros
    return [bairros]


# ---------------------- CALLBACK: ALTERAR MAPA BASE ----------------------

@app.callback(
    Output("camada-mapa-base", "children"),
    Input("btn-satelite", "n_clicks"),
    prevent_initial_call=True
)
def alternar_mapa_base(n_clicks):
    """
    Alterna entre mapa padrão e mapa satélite.
    """

    # Clique ímpar: mostra satélite
    if n_clicks % 2 == 1:
        return [tile_satelite]

    # Clique par: volta para mapa normal
    return [tile_mapa_padrao]


# ---------------------- EXECUÇÃO ----------------------

if __name__ == "__main__":
    import os
    port = int(os.getenv("PORT", 10000))
    app.run(host="0.0.0.0", port=port, debug=False)