import operator
import numpy
import random

def calcularDistancias(pesos, vector):
    distanciasEuclideas = {}
    vectorIndex = pesos.index(vector)           #Vamos a ignorar el indice del vector con el que estamos trabajando para no calcularle la distancia a si mismo
    for i in range(len(pesos) - 1):
        if i != vectorIndex:
            a = numpy.array(vector)
            b = numpy.array(pesos[i])
            distancia = numpy.linalg.norm(a-b)
            distanciasEuclideas[i] = distancia
    return distanciasEuclideas

def obtenerVecinos(vector, numVecinos):
    distancias = calcularDistancias(pesos, vector)
    distancias_sort = sorted(distancias.items(), key=operator.itemgetter(1))
    vecinos = []
    for d in distancias_sort:
        vecinos.append(d[0])
    return vecinos[0 : numVecinos]

def generarPoblacion(numIndividuos):
    poblacion = []
    for i in range(numIndividuos):
        cromosoma = []
        for i in range(30):
            gen = random.random()
            cromosoma.append(gen)
        poblacion.append(cromosoma)
    return poblacion 

pesos = [
    (0.2,0.8),
    (0.25,0.75),
    (0.41,0.59),
    (0.1,0.9),
    (0.5,0.5),
    (0.15,0.85),
    (0.97,0.03),
    (0.7,0.3),
    (0.65,0.35),
    (0.4,0.6)
]
#--------------------------------------------PRUEBAS------------------------------------------------------------------

'''
Calcular Distancias:

print("Vectores peso:", pesos)
pruebaDistancias = calcularDistancias(pesos, pesos[1])
'''

'''
Calcular Vecinos:

print("Distancia desde pesos1 a los demas:", pruebaDistancias)
pruebaVecinos = obtenerVecinos(pesos[1], 3)
print("Indice de pesos mas cercanos:", pruebaVecinos)
'''
poblacion = generarPoblacion(8)
print(poblacion)
