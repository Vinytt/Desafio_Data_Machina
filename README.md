# Desafio_Data_Machina
Desafio do processo seletivo Data Machina: Criar APIs funcionais para resolver os problemas propostos

## Problema 1: Distribuição Normal
O primeiro problema consistia em receber uma sequência qualquer de números e retornar uma lista em que cada elemento seria um o resultado da aplicação da função da distribuição normal sobre um dos números fornecidos na sequência.

### Usando o Programa
O código é uma API web que pode rodar um servidor local, e funciona através de requerimentos HTTP do tipo 'POST'.
 
Para usar o programa, execute o arquivo "api_problema1.py". Em seguida, mande um requerimento 'POST' para o endereço mostrado no terminal. O requerimento deve conter em seu corpo o a sequência que deve ser recebida pelo programa, passada em formato .json, como no exemplo abaixo.
 
#### Exemplo de requerimento
 
 Requerimento POST
 Endereço: http://127.0.0.1:5000/
 
 {"data" : [1, 0, 12, 40, 4, -3]}
 
#### Módulos usados
Flask (https://palletsprojects.com/p/flask/)
Numpy (https://numpy.org/)
 
## Problema 2.1: API de consulta de tempo e distância de viagens
O segundo problema requeria que fosse feita uma aplicação que recebesse uma cidade de origem e outra de destino (ambas capitais brasileiras), além do modal de tranporte e a hora da viagem. A partir destes dados, é esperado que o programa retorne a distância a ser percorrida em km e o tempo de viagem em horas.
 
### Usando o Programa
Para implementar o código foi necessário montar um banco de dados, guardado em um arquivo .txt "Capitais_db.txt", que armazena as distância entre trajetos das capitais brasileiras, tanto por via rodoviária quanto aérea. Este bando de dados foi montado com as informações do plug-in de mapas do "DuckDuckGO" (https://duckduckgo.com/?q=&atb=v248-1) e do site remanescente da empresa "Itatrans" (http://www.itatrans.com.br/distancia.html), agora adquirida pela "Agility".
 
Para rodar o código, execute o arquivo "api_problema2_1.py". Novamente, faça requerimentos do tipo 'POST' para o link mostrado, adicionando "info-percurso" ao final e forneça no corpo as informações da viagem a ser realizada em formato .json, como mostrado abaixo. A data de partida deve estar no formato "YYYY-MM-DD HH-MM", e os nomes das cidades NÃO podem ter acentos. Por fim, o modal deve ser um dentre "Rodovia" ou "Via Aerea".

#### Exemplo de Requerimento

Requerimento POST
Endereço: http://127.0.0.1:5000/info-percurso

{
  "partida" : "2021-05-29 12:00",
  "origem" : "Sao Paulo",
  "destino" : "Belem",
  "modal" : "Rodovia"
}

#### Módulos Usados
Flask (https://palletsprojects.com/p/flask/)
Datetime (https://docs.python.org/3/library/datetime.html)
Math (https://docs.python.org/3.8/library/math.html)
Python-TSP (https://pypi.org/project/python-tsp/)

## Problema 2.2: API de otimização de entrega
A segunda parte do segundo problema era baseada em fazer uma nova API, que receba uma lista de produtos com informações a respeito do nome do produto, valor, destino e data limite da entrega. Baseando-se nestar informações, o programa deve decidir qual é a melhor rota, saindo sempre de São Paulo.

### Usando o Programa
O problema da melhor rota é, por padrão, resolvido como um problema do caixeiro viajante (https://pt.wikipedia.org/wiki/Problema_do_caixeiro-viajante), de forma a escolher o caminho mais curto como o caminho ótimo. Também são usados como padrão a Via Aérea como modal de transporte e o dia 23 de Março de 2021 como data de partida (sem informação das horas).
Um funcionamento alternativo, porém menos eficiente, do programa é o de considerar também o lucro das viagens. Quando requerido para operar desta maneira, o programa usará a rota de maior lucro em detrimento da maior curta se a segunda for 30% menos lucrativa em comparação com a primeira.

Para mudar a forma de operação do programa, deve-se fazer um requerimento 'POST' ao link adicionando "param" ao final deste. O requerimento deve ter em seu corpo as alterações a serem feitas nos parâmetros padrões do código, em formato .json.

#### Exemplo de Requerimento - Mudando Parâmetros

Requerimento POST
Endereço: http://127.0.0.1:5000/param

{
  "modal" : "Rodovia",
  "data_partida" : "2021-05-29",
  "considerar_lucro" : "True"
}

#### Exemplo de Requerimento - Melhor Rota

Requerimento POST
Endereço: http://127.0.0.1:5000/melhor-rota

{ "produtos" :
    [
        {
            "nome_produto" : "refrigerante",
            "valor_entrega" : 400,
            "destino" : "Belem",
            "data_limite" : "2021-05-05"
        },
        
        {
            "nome_produto" : "desodorante",
            "valor_entrega" : 300,
            "destino" : "Belo Horizonte",
            "data_limite" : "2021-03-23"
        },

        {
            "nome_produto" : "demaquilante",
            "valor_entrega" : 200,
            "destino" : "Recife",
            "data_limite" : "2021-03-24"
        }

    ]
}

#### Módulos Usados:
Flask (https://palletsprojects.com/p/flask/)
Datetime (https://docs.python.org/3/library/datetime.html)
Math (https://docs.python.org/3.8/library/math.html)
Numpy (https://numpy.org/)
Python-TSP (https://pypi.org/project/python-tsp/)
Itertools (https://docs.python.org/3/library/itertools.html)
 
 
