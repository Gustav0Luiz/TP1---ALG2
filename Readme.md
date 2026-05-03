# Trabalho Prático 1 - Algoritmos II

## Explorador Comida di Buteco 2026 - BH

Este projeto foi desenvolvido para o Trabalho Prático 1 da disciplina de **Algoritmos II** (UFMG).

O objetivo principal é implementar uma estrutura de dados espacial, especificamente uma **árvore k-dimensional (k-d tree)**, para realizar **busca ortogonal em conjuntos de pontos**. No contexto do projeto, os pontos representam bares participantes do **Comida di Buteco 2026 em Belo Horizonte**, localizados por meio de coordenadas geográficas.

A aplicação final é um sistema interativo em Python que permite ao usuário informar um endereço, definir uma área de busca e visualizar no mapa os bares localizados dentro dessa região.

---

## Acesso ao Projeto

O projeto está disponível publicamente (código privado) no seguinte link:

**[Explorador Comida di Buteco - Render](https://tp1-alg2-maor.onrender.com/)**

---

## Contexto do Trabalho

O trabalho propõe a criação de um sistema para consulta de bares dentro de uma área retangular (ou circular), definida a partir de um endereço informado pelo usuário.

A base de dados utiliza bares participantes do Comida di Buteco 2026 em Belo Horizonte. Inicialmente, os dados possuem informações textuais de endereço. Para realizar buscas espaciais, os endereços são convertidos em coordenadas geográficas (latitude e longitude).

Após a conversão, os pontos são organizados em uma **k-d tree**, permitindo consultas por região de forma mais eficiente.

---

## Funcionalidades

Ao abrir a aplicação, o usuário visualiza um mapa interativo com os bares marcados como pinos de localização.

O sistema oferece:

- Visualização de todos os bares no mapa interativo
- Pesquisa de bares por endereço
- Definição do tamanho da área de busca (em km)
- Escolha entre busca retangular ou circular
- Visualização da região de busca desenhada no mapa
- Tabela de resultados filtrados
- Ordenação de bares por distância
- Reset de filtros e busca
- Alternância entre mapa padrão e satélite
- Visualização de contorno dos bairros de BH

---

## Busca Retangular

Na busca retangular, o usuário informa:

1. Um endereço
2. O comprimento da diagonal da região de busca (em quilômetros)

O sistema calcula os limites do retângulo e realiza uma busca ortogonal na k-d tree. Todos os bares localizados dentro da região são exibidos no mapa e na tabela.

---

## Busca Circular

Como funcionalidade extra, foi implementada a busca circular.

Nesse modo, o valor informado é interpretado como o **raio da busca** (em quilômetros). O sistema identifica bares dentro desse raio e utiliza a **fórmula de Haversine** para calcular a distância real entre o endereço e os bares encontrados.

---

## Dados Utilizados

Os dados dos bares foram fornecidos no arquivo `butecos_bh.csv`, contendo informações em formato textual. A API do **OpenStreetMap (Nominatim)** converte esses endereços em coordenadas geográficas, que são então utilizadas para construir a k-d tree.

---

## Tecnologias Utilizadas

| Tecnologia | Propósito |
|-----------|----------|
| **Python 3.10+** | Linguagem principal |
| **Dash & Dash Leaflet** | Framework web e mapas interativos |
| **Pandas** | Manipulação de dados |
| **GeoPy / Nominatim** | Geocodificação (endereço → coordenadas) |
| **OpenStreetMap** | Dados geográficos |
| **Render** | Hospedagem (backend privado) |

---

## Estrutura do Projeto

```
TP1---ALG2/
├── backend/
│   ├── data/
│   │   ├── butecos_bh.csv
│   │   └── address_search_cache.json
│   ├── scripts/
│   │   ├── addr_search.py
│   │   ├── populate_csv.py
│   │   └── fix_csv.py
│   └── src/
│       ├── kdtree.py
│       ├── osm.py
│       ├── config.py
│       └── utils.py
│
├── frontend/
│   ├── assets/
│   │   ├── style.css
│   │   └── [ícones e imagens]
│   ├── components/
│   │   └── map_components.py
│   ├── utils/
│   │   ├── config.py
│   │   ├── geo.py
│   │   └── table_components.py
│   └── main.py
│
├── requirements.txt
└── README.md
```

### Backend

Responsável por:
- Carregar dados dos bares
- Converter endereços em coordenadas geográficas
- Construir a k-d tree
- Realizar busca retangular/circular
- Calcular distâncias (Haversine)
- Retornar bares filtrados ao frontend

### Frontend

Responsável por:
- Exibir mapa interativo
- Receber entrada do usuário (endereço e alcance)
- Desenhar região de busca
- Exibir tabela de resultados
- Gerenciar interações visuais e camadas

---

## Como Executar Localmente

### 1. Clone o Repositório

```bash
git clone https://github.com/PHMGC/TP1---ALG2.git
cd TP1---ALG2
```

### 2. Crie um Ambiente Virtual (Recomendado)

```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate  # Windows
```

### 3. Instale as Dependências

```bash
pip install -r requirements.txt
```

### 4. Execute a Aplicação

```bash
python -m frontend.main
```

### 5. Acesse no Navegador

Após iniciar, abra seu navegador e acesse:

```
http://127.0.0.1:10000
```
---

## Configuração para Produção (Render)

A aplicação é automaticamente deployada no Render quando há push para a branch `main`.

O Render:
- Detecta a presença do `requirements.txt`
- Instala as dependências
- Executa: `python3 -m frontend.main`
- Lê a variável de ambiente `PORT` automaticamente (padrão: 10000)

**Repositório privado no GitHub** → Código protegido
**Aplicação pública no Render** → Interface acessível

---

## Observações Importantes

- A aplicação deve ser executada a partir da **raiz do projeto** para que os imports funcionem corretamente
- O arquivo `requirements.txt` contém todas as dependências necessárias
- A geocodificação depende de conexão com OpenStreetMap (Nominatim)
- O cache de endereços (`address_search_cache.json`) evita requisições repetidas à API
- Debug mode está desabilitado em produção

---

## Autores

- Gustavo Luiz A. R.
- Pedro H. M. G. Cortez (PHMGC)
