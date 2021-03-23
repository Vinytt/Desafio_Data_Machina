#Imports Necessários
from flask import Flask, request
from datetime import datetime, timedelta
from gerenciamento_dados_problema2 import ler_db_capitais, calcular_tempo, calcular_distancia, calcular_chegada
#----------------------------------------------------------------------

#Constantes
#Instancia uma API com nome 'Teste_Data_Machina':
app = Flask('Teste_21_Data_Machina')
#----------------------------------------------------------------------

#Rotas

#
@app.route('/info-percurso', methods=['POST'])
def info_percurso():
    #Cria o dicionário que será retornado
    dic_percurso = {"distancia" : '', "tempo estimado" : ''}

    #Recebe o body em formato json
    body = request.get_json()

    #Cria objeto datetime com a data/hora da partida no formato especificado:
    partida = datetime.strptime(body["partida"], "%Y-%m-%d %H:%M")
    origem = body["origem"]
    destino = body["destino"]
    modal = body["modal"]

    #Lê database de dados sobre as capitais
    dic_capitais = ler_db_capitais('Capitais_db.txt')

    #Calcula informações
    tempo = calcular_tempo(dic_capitais, origem, destino, modal)
    distancia = calcular_distancia(dic_capitais, origem, destino, modal)

    #string Tempo
    str_Tempo = str(tempo['horas']) + 'h' + str(tempo['minutos'])

    dic_percurso['distancia'] = str(distancia) + ' km'
    dic_percurso['tempo estimado'] = str_Tempo

    return dic_percurso
#----------------------------------------------------------------------

#Execução da API
app.run()
