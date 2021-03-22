#Imports Necessários
import numpy as np
#----------------------------------------------------------------------

#Funções

#Cacula distribuição normal num ponto x, usando média mi e desvio padrão dp
def calcular_dist_normal(x, mi, dp):
    #Numerador
    numerador = np.exp(-0.5 *(((x - mi) / dp)) ** 2 )
    #Denominador
    denominador = dp * np.sqrt(2 * np.pi)

    dist_normal = numerador / denominador
    print(dist_normal)

    return dist_normal
