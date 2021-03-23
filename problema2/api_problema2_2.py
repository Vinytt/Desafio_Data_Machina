#Imports Necessários
from flask import Flask, request
from datetime import datetime, timedelta
from gerenciamento_dados_problema2 import ler_db_capitais, calcular_tempo, calcular_distancia, calcular_chegada, rota_mais_curta, lucro_rota, rota_mais_lucrativa
#----------------------------------------------------------------------

#Constantes
#Instancia uma API com nome 'Teste_Data_Machina':
app = Flask('Teste_22_Data_Machina')
modal = "Via Aerea"
data_partida = datetime(year=2021, month=3, day=23)
considerar_lucro = False
#----------------------------------------------------------------------

#Rotas

#Calcula melhor ordem de viagens
@app.route('/melhor-rota', methods = ['POST'])
def caixeiro_lucrativo():
    #Recebe o body em formato json
    body = request.get_json()

    lista_produtos = body["produtos"]

    #Lê database com os dados das capitais
    dic_capitais = ler_db_capitais()

    #Rota mais curta
    rota_curta = rota_mais_curta(dic_capitais, lista_produtos, modal)

    #Lucro da rota
    lucro_rota_curta = lucro_rota(dic_capitais, rota_curta, data_partida, lista_produtos, modal)

    #Rota a ser seguida
    rota = rota_curta

    if considerar_lucro:
        #Rota mais lucrativa
        rota_lucra, maior_lucro = rota_mais_lucrativa(dic_capitais, lista_produtos, data_partida, modal)

        if maior_lucro * 0.7 >= lucro_rota_curta:
            rota = rota_lucra


    return 'As cidades a serem visitadas, começando pela partida (São Paulo), são:\n' + str(rota)

#Definir modal, data de partida e a consideração do lucro
@app.route('/param', methods = ['POST'])
def definir_parametros():
    #Recebe o body em formato json
    body = request.get_json()

    modal = body["modal"]
    data_partida = datetime.strptime(body["data_partida"], "%Y-%m-%d")
    considerar_lucro = body["considerar_lucro"] == "True"

    return 'Parametros mudados:\n' + modal + '\n' + str(data_partida) + '\n' + str(considerar_lucro)
#----------------------------------------------------------------------

#Execução da API
app.run()
