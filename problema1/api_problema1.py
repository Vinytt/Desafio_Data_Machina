#Imports Necessários
from flask import Flask, request
from gerenciamento_dados_problema1 import calcular_dist_normal
#----------------------------------------------------------------------

#Constantes
#Instancia uma API com nome 'Teste_Data_Machina':
app = Flask('Teste_1_Data_Machina')
#----------------------------------------------------------------------

#Rotas

#Gera uma distribuição normal com média 0 e desvio padrão 1 a partir dos
#dados recebidos pelo body do request
@app.route('/', methods = ['POST'])
def gerar_dist_normal():
    #Recebe o body em formato json
    body = request.get_json()
    sequencia = body["data"]

    #variável que guardará a sequência convertida na distribuição normal
    seq_dist_normal = []

    #iterar por cada elemento da sequência e calcular a conversão
    for num in sequencia:
        dist_normal = calcular_dist_normal(num, 0, 1)
        seq_dist_normal.append(dist_normal)

    return {'outup' : seq_dist_normal}
#----------------------------------------------------------------------

#Execução da API
app.run()
