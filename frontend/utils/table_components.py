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

        style_table={
            "overflowX": "auto",
            "borderRadius": "14px",
            "overflow": "hidden",
            "boxShadow": "0 4px 14px rgba(0, 0, 0, 0.10)",
            "border": "1px solid #f3d1bd",
        },

        style_header={
            "backgroundColor": "#fc802d",
            "color": "#111827",
            "fontWeight": "700",
            "fontFamily": "Inter, Arial, sans-serif",
            "fontSize": "14px",
            "padding": "12px",
            "border": "none",
            "textAlign": "center",
        },

        style_cell={
            "fontFamily": "Inter, Arial, sans-serif",
            "fontSize": "14px",
            "padding": "12px",
            "textAlign": "left",
            "whiteSpace": "normal",
            "height": "auto",
            "border": "none",
            "borderBottom": "1px solid #f1f1f1",
            "color": "#1f2937",
        },

        style_data={
            "backgroundColor": "#ffffff",
        },

        style_data_conditional=[
            {
                "if": {"row_index": "odd"},
                "backgroundColor": "#fff7ed",
            },
            {
                "if": {"state": "active"},
                "backgroundColor": "#ffedd5",
                "border": "1px solid #fc802d",
            },
            {
                "if": {"state": "selected"},
                "backgroundColor": "#ffedd5",
                "border": "1px solid #fc802d",
            },
            {
                "if": {"column_id": "distancia_km"},
                "textAlign": "center",
                "fontWeight": "700",
                "color": "#fc802d",
            },
            {
                "if": {"column_id": "nome"},
                "fontWeight": "700",
            },
        ],

        style_cell_conditional=[
            {
                "if": {"column_id": "nome"},
                "width": "22%",
            },
            {
                "if": {"column_id": "endereco"},
                "width": "60%",
            },
            {
                "if": {"column_id": "distancia_km"},
                "width": "18%",
            },
        ],
    )