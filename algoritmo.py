from cmath import pi, sin, sqrt
import operator
import numpy
import random

#------------------------------------------------INICIALIZACION--------------------------------------------------------

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
    (0.4,0.6),
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

#----------------------------------OPERACIONES DE VECTORES Y POBLACION-------------------------------------------------

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

def generarPoblacion(numIndividuos=len(pesos)):
    poblacion = []
    for i in range(numIndividuos):
        cromosoma = []
        for i in range(30):
            gen = random.random()
            cromosoma.append(round(gen, 5))       #Numero de decimales a utilizar
        poblacion.append(cromosoma)
    return poblacion

#----------------------------------------EVALUACION DE INDIVIDUO------------------------------------------------------

def g(x):
    suma = 0
    for i in range(1, len(x)):
        suma = suma + x[i]
    return 1 + (9*suma/(len(x) - 1))

def h(x):
    f1 = x[0]
    g = g(x)
    return 1 - (sqrt(f1/g)) - (f1/g)*sin((10*pi*f1))

def f2(x):
    return g(x) * h(x)

def z(poblacion):
    f1 = 100.00
    f2 = 100.00
    for x in poblacion:
        if x[0] < f1:
            f1 = x[0]
        if f2(x) < f2:
            f2 = f2(x)
    return (f1, f2)

def gte(x, poblacion, pesos): #Funcion a minimizar
    index = poblacion.index(x)
    w = pesos[index]
    z = z(poblacion)
    f1 = x[0]
    f2 = f2(x)
    argumento1 = w[0] * abs(f1 - z[0])
    argumento2 = w[1] * abs(f2 - z[1])
    return max(argumento1, argumento2)

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

#Generar poblacion aleatoria:

poblacion = generarPoblacion()
print(poblacion)


