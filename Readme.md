### Trabalho Prático 1 - Disciplina de Algoritmos 2

- O objetivo do trabalho é a implementação de árvores k-dimensionais para realização de busca ortogonal em conjuntos de pontos.

#### O que deve ser feito?

-  implementar um sistema para consulta de bares dentro de uma área retangular com base no endereço dado como entrada pelo usuário.

- criar um sistema interativo para visualizar os bares participantes do Comida Di Buteco de 2026. O sistema deve exibir os bares como pinos de localização no mapa da cidade. As informações de nome do bar, endereço, e
distância do endereço informado também deverão ser exibidas em uma tabela abaixo do mapa.

#### Especificações de projeto:

- O usuário deverá informar um endereço em uma barra de busca, que será utilizado
como centro para a definição de uma região retangular de interesse. Todos os bares
localizados dentro dessa região deverão ser identificados, e a tabela exibida abaixo do
mapa deverá ser filtrada de acordo com esses resultados, que deverão ser
apresentados em ordem crescente de distância em relação ao endereço informado. 

- O tamanho da área de busca será determinado pelo comprimento da diagonal do
retângulo, valor também fornecido pelo usuário. A projeção desse retângulo no mapa
e, consequentemente, a seleção dos bares nele contidos serão realizadas com o
suporte de uma árvore k-dimensional (k-d tree), utilizando as coordenadas geográficas
(latitude e longitude) como dimensões do espaço

- A implementação deverá ser feita obrigatoriamente em Python. O sistema deverá ser
efetivamente interativo, permitindo definir e ajustar um endereço e o tamanho do retângulo da busca ortogonal

- *O produto final deverá ser uma página interativa que permite a visualização dos dados, filtragem por endereço e distância, e eventuais resets dos filtros. As páginas serão hospedadas no Github Pages.*


#### Dados utilizados:

- Os dados foram disponibilizados no arquivo butecos_bh.csv, entretanto apenas recebemos o endereço (rua, bairro número etc). Precisamos utilizar a API do OpenStreetMaps para converter os endereços em coordenadas geográficas exatas (talvez salvar as coordenadas de todos os bares de uma vez, ao invés de toda hora fazer requisições).


#### Pontos Extra:

- Utilizar um círculo no lugar de um retângulo.