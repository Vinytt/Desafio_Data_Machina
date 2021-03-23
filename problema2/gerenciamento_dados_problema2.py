#Imports Necessários
from datetime import datetime, timedelta
from math import modf
import numpy as np
from python_tsp.exact import solve_tsp_dynamic_programming
from itertools import permutations
#----------------------------------------------------------------------

#Constantes
dic_vel = {'Rodovia' : 90, 'Via Aerea' : 800}
dic_modais = {'Rodovia' : 'km_rodovia', 'Via Aerea' : 'km_aerea'}
#----------------------------------------------------------------------

#Funções

#Lê documento de texto com as informações das cidades e a distância entre elas
def ler_db_capitais(nome_arq = 'Capitais_db.txt'):
    Capitais_db = open(nome_arq, 'r')
    conteudo = Capitais_db.readlines()
    #Dicionário que irá mapear a distância entre as cidades:
    dic_capitais = {}

    #Ler conteúdo do arquivo
    for linha in conteudo:

        i_virgula = linha.find(',') #indica a linha com os nomes das cidades
        i_km_rodovia = linha.find('km_rodovia=') #indica a linha com a distância de um percurso pela rodovia
        i_km_aerea = linha.find('km_aerea=') #indica a linha com a distância de um percurso por via aérea

        #Nome das cidades
        if i_virgula != -1:
            cidade1 = linha[:i_virgula]
            cidade2 = linha[i_virgula + 1:len(linha) - 1]
            #Criaremos um dicionário para cada dupla de cidades:
            dic_cidades = {'km_rodovia' : 0, 'km_aerea' : 0}

        #Distância Rodovia
        elif i_km_rodovia != -1:
            km_rodovia = int(linha[i_km_rodovia + len('km_rodovia='):])
            dic_cidades['km_rodovia'] = km_rodovia

        #Distância Via Aérea
        elif i_km_aerea != -1:
            km_aerea = int(linha[i_km_aerea + len('km_aerea='):])
            #print(km_aerea)
            dic_cidades['km_aerea'] = km_aerea

        #Colocamos dados no dicionário principal
        else:
            dic_capitais[cidade1 + ',' + cidade2] = dic_cidades

    return dic_capitais

#Calcular o tempo (em horas) de viagem entre duas cidades
def calcular_tempo(dic_capitais, origem, destino, modal):

    dic_tempo = {'horas' : 0, 'minutos' : 0}

    if origem < destino:
        cidade1 = origem
        cidade2 = destino
    else:
        cidade1 = destino
        cidade2 = origem

    chave = dic_modais[modal]
    velocidade = dic_vel[modal]

    horas = dic_capitais[cidade1 + ',' + cidade2][chave] / velocidade

    minutos = int(modf(horas)[0] * 60)
    horas = int(modf(horas)[1])

    dic_tempo['horas'] = horas
    dic_tempo['minutos'] = minutos

    return dic_tempo

#Calcular a distância de um trajeto entre duas cidades
def calcular_distancia(dic_capitais, origem, destino, modal):

    if origem < destino:
        cidade1 = origem
        cidade2 = destino
    else:
        cidade1 = destino
        cidade2 = origem

    chave = dic_modais[modal]
    velocidade = dic_vel[modal]

    return dic_capitais[cidade1 + ',' + cidade2][chave]

#Calcular data de chegada de uma viagem entre duas cidades
def calcular_chegada(duracao, hora_partida):

    hora_chegada = hora_partida + timedelta(hours = duracao['horas'], minutes = duracao['minutos'])

    return hora_chegada

#Calcula o ciclo hamiltoniano mais curto, partindo de São Paulo e voltando para São Paulo (rota cíclica)
#Retorna uma lista com os nomes da cidade, em ordem
def rota_mais_curta(dic_capitais, lista_produtos, modal):
    #Matriz de distâncias entre as cidades
    matriz_dist = []

    #Vetor de distância para São Paulo especificamente
    dist_sp = [0]

    #Monta vetor de distância para SP
    for produto in lista_produtos:
        d = calcular_distancia(dic_capitais, 'Sao Paulo', produto["destino"], modal)
        dist_sp.append(d)

    matriz_dist.append(dist_sp)

    #Monta vetor de distância para cada cidade
    for produto in lista_produtos:
        vetor_dist = []
        d = calcular_distancia(dic_capitais, 'Sao Paulo', produto["destino"], modal)
        vetor_dist.append(d)
        for outro_prod in lista_produtos:
            if produto["destino"] == outro_prod["destino"]:
                d = 0
            else:
                d = calcular_distancia(dic_capitais, produto["destino"], outro_prod["destino"], modal)
            vetor_dist.append(d)

        matriz_dist.append(vetor_dist)

    #Transforma numa matriz np
    np_matriz_dist = np.array(matriz_dist)

    #Calcula rota mais curta, com cada cidade (nó) representado por números
    rota, distancia_total = solve_tsp_dynamic_programming(np_matriz_dist)

    #Dicionário para traduzir os números para nomes de cidade
    dic_rota = {0 : 'Sao Paulo'}

    #Monta dicionário
    for i in range(1, len(lista_produtos) + 1):
        dic_rota[i] = lista_produtos[i - 1]["destino"]

    rota_nomes = []

    for num in rota:
        rota_nomes.append(dic_rota[num])

    #Retorna uma lista com as cidades que devem ser visitadas, em ordem e
    #começando por São Paulo
    return rota_nomes

#Busca uma lista de dicionários 'produto' em busca de uma cidade específica
#retorna o índice da lista
def achar_produto_cidade(lista_produtos, cidade):
    for i in range(len(lista_produtos)):
        if lista_produtos[i]["destino"] == cidade:
            return i

    return None

#Dada uma rota, calcula o lucro a ser obtido dela
#OBS: data_partida já tem que ser um objeto datetime!!!
def lucro_rota(dic_capitais, rota, data_partida, lista_produtos, modal):
    #Percorrer rota e calcular o lucro
    lucro = 0

    for i in range(len(rota) -1):
        #calcular a data de chegada
        dic_tempo = calcular_tempo(dic_capitais, rota[i], rota[i + 1], modal)
        data_chegada = calcular_chegada(dic_tempo, data_partida)

        #Pega o índice do produto que vai para esta cidade na lista
        i_cidade = achar_produto_cidade(lista_produtos, rota[i + 1])

        #Pega data limite, transformando em objeto datetime
        data_limite = datetime.strptime(lista_produtos[i_cidade]["data_limite"], "%Y-%m-%d")

        #Se o prazo não venceu:
        if data_limite >= data_chegada:
            lucro += float(lista_produtos[i_cidade]["valor_entrega"])
        else:
            lucro += float(lista_produtos[i_cidade]["valor_entrega"] / 2)

        #Atualiza data de partida para ser a data de chegada na próxima cidade
        data_partida = data_chegada

    return lucro

#Calcula qual é a rota mais lucrativa possível
#Retorna uma lista com os nomes das cidades, em ordem
def rota_mais_lucrativa(dic_capitais, lista_produtos, data_partida, modal):
    #Maior lucro encontrado
    maior_lucro = 0

    #Sim, vamos percorrer as rotas possíveis na força bruta...
    lista_cidades = []
    for produto in lista_produtos:
        lista_cidades.append(produto["destino"])

    #Cria uma lista de permutações das cidades fora São Paulo
    permut_cidades = []
    for per in permutations(lista_cidades, len(lista_cidades)):
        permut_cidades.append(list(per))

    for rota in permut_cidades:
        lucro = lucro_rota(dic_capitais, ['Sao Paulo'] + rota, data_partida, lista_produtos, modal)
        if lucro >= maior_lucro:
            maior_lucro = lucro
            rota_maior_lucro = ['Sao Paulo'] + rota

    print(maior_lucro)
    print(rota_maior_lucro)
    return rota_maior_lucro, maior_lucro
