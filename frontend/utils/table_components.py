"""
utils/table_components.py

Responsabilidade do arquivo:
- Centralizar tudo que está relacionado à tabela de resultados.
- Transformar os bares retornados pelo orquestrador em dados para a tabela.
- Criar o componente visual dash_table.DataTable.

Este arquivo espera receber os bares já filtrados pelo backend/orquestrador.

O orquestrador deve retornar uma lista de bares contendo, no mínimo:
- name
- street
- number
- district
- city_state
- distance_km

A filtragem e ordenação ficam no backend/orquestrador.
"""


from dash import dash_table


def CreateTableDataFromResults(bares_filtrados):
    """
    Cria os dados da tabela a partir dos bares retornados pelo orquestrador.

    Os bares já devem vir:
    - filtrados dentro da área de busca;
    - com a distância calculada;
    - ordenados por distância crescente.
    """

    linhas_tabela = []

    for bar in bares_filtrados:
        endereco = f"{bar.get('street', '')}"

        if bar.get("number"):
            endereco += f", {bar['number']}"

        district = bar.get("district", "")
        city_state = bar.get("city_state", "")

        if district or city_state:
            endereco += f" - {district}, {city_state}"

        linhas_tabela.append({
            "nome": bar.get("name", ""),
            "endereco": endereco,
            "distancia_km": round(float(bar.get("distance_km", 0)), 2)
        })

    return linhas_tabela


def create_tabela_resultados(dados_tabela_inicial=None):
    """
    Cria o componente visual da tabela de resultados.

    A tabela começa vazia ou com os dados recebidos.
    Depois, o callback no main.py atualiza a propriedade data
    do componente com id="tabela-bares".
    """

    if dados_tabela_inicial is None:
        dados_tabela_inicial = []

    return dash_table.DataTable(
        id="tabela-bares",

        columns=[
            {"name": "Bar", "id": "nome"},
            {"name": "Endereço", "id": "endereco"},
            {"name": "Distância (km)", "id": "distancia_km"}
        ],

        data=dados_tabela_inicial,

        # Mantemos sem ordenação nativa para não exibir setas no cabeçalho.
        sort_action="none",

        page_size=10,

        fill_width=True,

        style_table={
            "overflowX": "auto",
            "borderRadius": "18px",
            "overflow": "hidden",
            "boxShadow": "0 8px 24px rgba(90, 45, 10, 0.12)",
            "border": "1px solid #f1d3bf",
            "backgroundColor": "#fffaf5",
        },

        style_header={
            "backgroundColor": "#fc802d",
            "color": "#ffffff",
            "fontWeight": "800",
            "fontFamily": "Inter, Arial, sans-serif",
            "fontSize": "15px",
            "padding": "14px 12px",
            "border": "none",
            "textAlign": "center",
        },

        style_cell={
            "fontFamily": "Inter, Arial, sans-serif",
            "fontSize": "14px",
            "padding": "14px 14px",
            "textAlign": "left",
            "whiteSpace": "normal",
            "height": "auto",
            "border": "none",
            "borderBottom": "1px solid #f3ede7",
            "color": "#1f2937",
            "lineHeight": "1.4",
        },

        style_data={
            "backgroundColor": "#ffffff",
        },

        style_data_conditional=[
            {
                "if": {"row_index": "odd"},
                "backgroundColor": "#fff8f1",
            },
            {
                "if": {"state": "active"},
                "backgroundColor": "#fff0e6",
                "border": "1px solid #fc802d",
            },
            {
                "if": {"state": "selected"},
                "backgroundColor": "#fff0e6",
                "border": "1px solid #fc802d",
            },
            {
                "if": {"column_id": "distancia_km"},
                "textAlign": "center",
                "fontWeight": "800",
                "color": "#e66f21",
                "fontSize": "15px",
            },
            {
                "if": {"column_id": "nome"},
                "fontWeight": "800",
            },
        ],

        style_cell_conditional=[
            {
                "if": {"column_id": "nome"},
                "width": "22%",
                "textAlign": "left",
            },
            {
                "if": {"column_id": "endereco"},
                "width": "60%",
                "textAlign": "left",
            },
            {
                "if": {"column_id": "distancia_km"},
                "width": "18%",
                "textAlign": "center",
            },
        ],

        css=[
            {
                "selector": ".dash-table-container .dash-spreadsheet-container",
                "rule": "border-radius: 18px; overflow: hidden;"
            },
            {
                "selector": ".dash-spreadsheet td div",
                "rule": "display: block;"
            },
            {
                "selector": ".previous-next-container",
                "rule": "margin-top: 10px;"
            }
        ],
    )