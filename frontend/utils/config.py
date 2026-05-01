"""
utils/config.py

Responsabilidade do arquivo:
- Centralizar constantes e configurações globais do projeto.
- Guardar valores usados em diferentes partes do sistema, como:
    - coordenada inicial do mapa;
    - valor padrão da diagonal/alcance;
    - configuração do ícone personalizado dos bares.

Quando precisar alterar uma configuração padrão, altere aqui.
"""


# Coordenada central inicial.
# Atualmente aponta para a região da Praça Raul Soares, em Belo Horizonte.
LAT = -19.922760
LON = -43.945162


# Valor inicial usado como alcance padrão da busca.
# No retângulo, esse valor representa a diagonal em km.
# No círculo, se usado, pode representar o raio em km.
DIAGONAL_KM = 5


# Ícone personalizado dos bares.
# A imagem deve estar em:
# assets/pin.png
custom_icon_bar_pin = {
    "iconUrl": "/assets/pin.png",
    "iconSize": [60, 60],
    "iconAnchor": [30, 60],
    "popupAnchor": [0, -55],
    "tooltipAnchor": [0, -45]
}

custom_icon_search_pin = {
    "iconUrl": "/assets/search_pin.png",
    "iconSize": [60, 60],
    "iconAnchor": [30, 60],
    "popupAnchor": [0, -55],
    "tooltipAnchor": [0, -45]
}