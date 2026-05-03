# Trabalho Prático 1 - Algoritmos II

## Explorador Comida di Buteco 2026 - BH

Este projeto foi desenvolvido para o Trabalho Prático 1 da disciplina de **Algoritmos II**.

O objetivo principal do trabalho é implementar uma estrutura de dados espacial, especificamente uma **árvore k-dimensional (k-d tree)**, para realizar **busca ortogonal em conjuntos de pontos**. No contexto do projeto, os pontos representam bares participantes do **Comida di Buteco 2026 em Belo Horizonte**, localizados por meio de coordenadas geográficas.

A aplicação final é um sistema interativo em Python que permite ao usuário informar um endereço, definir uma área de busca e visualizar no mapa os bares localizados dentro dessa região.

---

## Acesso ao projeto

O projeto está disponível publicamente no seguinte link:

https://tp1-alg2-maor.onrender.com/

---

## Contexto do trabalho

O trabalho propõe a criação de um sistema para consulta de bares dentro de uma área retangular, definida a partir de um endereço informado pelo usuário.

A base de dados utilizada contém bares participantes do Comida di Buteco 2026 em Belo Horizonte. Inicialmente, os dados dos bares possuem informações textuais de endereço, como rua, número, bairro e cidade. Para que seja possível realizar buscas espaciais, esses endereços são convertidos em coordenadas geográficas, representadas por latitude e longitude.

Após essa conversão, os pontos são organizados em uma k-d tree. Essa estrutura permite realizar consultas por região de forma mais eficiente do que verificar todos os bares um por um.

---

## Funcionamento do sistema

Ao abrir a aplicação, o usuário visualiza um mapa interativo com os bares participantes marcados como pinos de localização.

O sistema permite:

- visualizar todos os bares no mapa;
- pesquisar um endereço;
- definir o tamanho da área de busca;
- escolher entre busca retangular e busca circular;
- visualizar a região de busca desenhada no mapa;
- filtrar os bares localizados dentro da região;
- exibir os resultados em uma tabela;
- ordenar os bares encontrados por distância em relação ao endereço pesquisado;
- limpar a busca e voltar à visualização inicial;
- alternar entre mapa padrão e mapa satélite (disponível apenas quando executado localmente);
- ativar ou desativar a camada com contorno dos bairros de Belo Horizonte.

---

## Busca retangular

Na busca retangular, o usuário informa:

1. um endereço;
2. o comprimento da diagonal da região de busca, em quilômetros.

O endereço informado é convertido em coordenadas geográficas e utilizado como centro da região. A partir da diagonal digitada, o sistema calcula os limites do retângulo e realiza uma busca ortogonal na k-d tree.

Todos os bares localizados dentro da região são retornados e exibidos no mapa e na tabela.

---

## Busca circular

Como funcionalidade extra, também foi implementada a busca circular.

Nesse modo, o valor informado pelo usuário é interpretado como o raio da busca, em quilômetros. O sistema identifica os bares localizados dentro desse raio e utiliza a fórmula de Haversine para calcular a distância real entre o endereço pesquisado e os bares encontrados.

---

## Dados utilizados

Os dados dos bares foram fornecidos no arquivo:

```text
butecos_bh.csv
```

A base original possui os endereços dos bares em formato textual. Para transformar esses endereços em coordenadas geográficas, foi utilizada a API do OpenStreetMap por meio da biblioteca GeoPy/Nominatim.

As coordenadas obtidas são utilizadas como entrada para a construção da k-d tree.

---

## Tecnologias utilizadas

- Python
- Dash
- Dash Leaflet
- Dash Extensions
- Pandas
- GeoPy
- OpenStreetMap / Nominatim
- HTML/CSS
- Render

---

## Estrutura do projeto

A estrutura principal do projeto está organizada em backend e frontend:

```text
tp1/
├── backend/
│   ├── data/
│   ├── scripts/
│   └── src/
│
├── frontend/
│   ├── assets/
│   ├── components/
│   ├── utils/
│   └── main.py
│
├── requirements.txt
├── README.md

```

### Backend

O backend é responsável por:

- carregar os dados dos bares;
- converter endereços em coordenadas;
- construir a k-d tree;
- realizar a busca retangular;
- realizar a busca circular;
- calcular distâncias;
- retornar os bares filtrados para o frontend.

### Frontend

O frontend é responsável por:

- exibir o mapa interativo;
- exibir os bares como marcadores;
- receber o endereço e o alcance informados pelo usuário;
- desenhar a região de busca;
- exibir a tabela de resultados;
- controlar botões, camadas e interações visuais.

---

## Como executar localmente

Além do acesso público pelo link do Render, o projeto também pode ser executado localmente.

### 1. Clone o repositório

```bash
git clone https://github.com/PHMGC/TP1---ALG2.git
cd tp1
```

---


### 2. Instale as dependências

O projeto possui um arquivo `requirements.txt` com as dependências necessárias.

Execute:

```bash
pip install -r requirements.txt
```

---

### 5. Execute a aplicação

A execução deve ser feita a partir da pasta raiz do projeto.

```bash
python -m frontend.main
```

---

### 6. Acesse no navegador

Após iniciar a aplicação, abra o navegador e acesse:

```text
http://127.0.0.1:8050
```

---

## Observações importantes

- A aplicação deve ser executada a partir da raiz do projeto para que os imports entre `frontend` e `backend` funcionem corretamente.
- O arquivo `requirements.txt` deve ser utilizado para instalar todas as dependências necessárias.
- O sistema utiliza geocodificação por meio do OpenStreetMap/Nominatim.

---


## Autores

- Gustavo Luiz A. R.
- Pedro H.
