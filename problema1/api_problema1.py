#Imports Necessários
from flask import Flask, request
#----------------------------------------------------------------------

#Constantes
#Instancia uma API com nome 'Teste_Data_Machina':
app = Flask('Teste_Data_Machina')
#----------------------------------------------------------------------

#Rotas

#Gera uma distribuição normal com média 0 e desvio padrão 1 a partir dos
#dados recebidos pelo body do request
@app.route('/', methods = ['POST'])
def gerar_dist_normal():
    #Recebe o body em formato json
    body = request.get_json()
    sequencia = body["data"]
    dist_normal = yey()

    return {'outup' : dist_normal}
