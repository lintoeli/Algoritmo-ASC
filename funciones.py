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
    distanciasOrdenadas = sorted(distancias.items(), key=operator.itemgetter(1))
    vecinos = []
    for d in distanciasOrdenadas:
        vecinos.append(d[0])
    return vecinos[0 : numVecinos]

def generarPoblacion(numIndividuos=len(pesos)):
    poblacion = []
    for i in range(numIndividuos):
        cromosoma = []
        for i in range(30):
            gen = random.random()
            cromosoma.append(gen)       #Numero de decimales a utilizar para cada gen
        poblacion.append(cromosoma)
    return poblacion

def sumarIndividuos(x, y):
    z = []
    for i in range(len(x)):
        z.append(x[i] + y[i])
    return z

def restarIndividuos(x, y):
    z = []
    for i in range(len(x)):
        z.append(x[i] - y[i])
    return z

def individuoPorConstante(x, c):
    for i in range(len(x)):
        x[i] = x[i]*c
    return x

def corregirIndividuo(x):           #Esto es para que in individuo no tenga atributos por fuera del rango disponible
    for i in range(len(x)):
        if x[i] < 0:
            x[i] = 0
        elif x[i] > 1:
            x[i] = 1
    

#----------------------------------------EVALUACION DE INDIVIDUO Y GENERACION------------------------------------------------------

def funcionG(x):
    suma = 0
    for i in range(1, len(x)):
        suma = suma + x[i]
    return 1 + (9*suma/(len(x) - 1))

def funcionH(x):
    f1 = x[0]
    g = funcionG(x)
    return 1 - (sqrt(f1/g)) - (f1/g)*sin((10*pi*f1))

def funcionF2(x):
    f2 = funcionG(x) * funcionH(x)
    return f2.real                       #Hay veces que al calcular f2 sale un numero complejo del tipo a + 0*i, lo que impide la ejecucion del if de la funcion Z de abajo

def funcionZ(poblacion):
    f1 = 100.0
    f2 = 100.0
    for i in range(len(poblacion)):
        x = poblacion[i]
        f1Aux = x[0]
        f2Aux = funcionF2(x)
        if f1Aux < f1:
            f1 = f1Aux
        if f2Aux < f2:
            f2 = f2Aux
    tupla = (f1,f2)
    return tupla

def gte(x, poblacion, pesos, i):          #FITNESS
    z = funcionZ(poblacion)
    w = pesos[i]
    f1 = x[0]
    f2 = funcionF2(x)
    argumento1 = w[0] * abs(f1 - z[0])
    argumento2 = w[1] * abs(f2 - z[1])
    return max(argumento1, argumento2)

def evaluarGeneracion(poblacion, pesos):        #Obtenemos una lista ordenada por los mejores valores (los mas bajos)
    lista = []
    for i in range(len(poblacion)):
        x = poblacion[i]
        fitness = gte(x, poblacion, pesos, i)
        lista.append((i, fitness))
    listaFinal = sorted(lista, key=operator.itemgetter(1))
    return listaFinal

def compararFitness(x, y, poblacion, i):
    fit1 = gte(x, poblacion, pesos, i)
    fit2 = gte(y, poblacion, pesos, i)
    if fit1 < fit2:
        return x
    else: 
        return y

def mejorIndividuoGlobal(registroFitness):
    items = list(registroFitness.items())               #Si no se castea a list falla, da un error
    mejorFitness = 1000                                 #'dict_items' object is not subscriptable
    res0 = 0                                            
    res1 = 0
    for i in range(len(items)):
        poblacion = items[i][1]
        for j in range(len(poblacion)):
            x = poblacion[j]
            if x[1] <= mejorFitness:
                mejorFitness = x[1]
                res0 = i
                res1 = j                                #Devolvemos una lista que contiene la generacion,
    return [res0, res1, mejorFitness]                   #el indice del individuo de esa generacion y el fitness

#-----------------------------------------------------------------CRUCE Y MUTACION-----------------------------------------------------------------

def mutacionConVecinos(x, poblacion, pesos):
    indiceX = poblacion.index(x)
    pesoX = pesos[indiceX]                         #Obtenemos la vecindad completa de un individuo
    vecinosX = obtenerVecinos(pesoX, 3)            #NumVecinos = 3   
    vecinosX.append(indiceX)                       # + 1 vecino que es el propio individuo = 4 vecinos
    
    n1 = random.choice(vecinosX)
    x1 = poblacion[n1]                              #Seleccionamos 3 elementos aleatoriamente de la
    vecinosX.remove(n1)                             #vecindad
    n2 = random.choice(vecinosX)
    x2 = poblacion[n2]                              #Vamos eliminando elementos de la lista para no
    vecinosX.remove(n2)                             #repetir individuos
    n3 = random.choice(vecinosX)                    
    x3 = poblacion[n3] 
    vecinosX.remove(n3)

    aux1 = restarIndividuos(x2, x3)               #x2 - x3
    aux2 = individuoPorConstante(aux1, 0.5)       #F(x2 - x3)
    aux3 = sumarIndividuos(x1, aux2)              #x1 + F(x2 - x3)
    corregirIndividuo(aux3)
    return aux3
    
def cruce1(x, poblacion, pesos, probabilidad):     
    v = mutacionConVecinos(x, poblacion, pesos)
    y = []                                        
    for i in range(len(x)):
        p = random.random()                       #Se genera un numero aleatorio para decidir si el nuevo valor
        if p >= probabilidad:                     #del proximo individuo sera del individuo original o del mutado
            y.append(x[i])
        else:
            y.append(v[i])
    return y

def cruce2(x1, x2, probabilidad):     
    y = []                                        
    for i in range(len(x1)):
        p = random.random()                       #Se genera un numero aleatorio para decidir si el nuevo valor
        if p >= probabilidad:                     #del proximo individuo sera del individuo original o del mutado
            y.append(x1[i])
        else:
            y.append(x2[i])
    return y

#--------------------------------------------PRUEBAS------------------------------------------------------------------------

'''
#Calcular Distancias:

print("Vectores peso:", pesos)
pruebaDistancias = calcularDistancias(pesos, pesos[1])
'''

'''
#Calcular Vecinos:

print("Distancia desde pesos1 a los demas:", pruebaDistancias)
pruebaVecinos = obtenerVecinos(pesos[1], 3)
print("Indice de pesos mas cercanos:", pruebaVecinos)
'''
'''
#Generar poblacion aleatoria:

poblacion = generarPoblacion()
print(poblacion)
'''

'''
#Evaluar un individuo:

poblacionPrueba = generarPoblacion()
print(poblacionPrueba)

x = poblacionPrueba[0]
print(x)

f2 = funcionF2(x)
print("f1=", x[0], ", f2=", f2)

z = funcionZ(poblacionPrueba)
print("z= ", z)

evaluacionX = gte(x, poblacionPrueba, pesos)
print("Puntuacion del individuo= ", evaluacionX)
'''

'''
#Evaluar una generacion:

poblacionPrueba = generarPoblacion()
print(poblacionPrueba)

evaluacionG = evaluarGeneracion(poblacionPrueba, pesos)
print("Puntuaciones de la generacion actual: ", evaluacionG)
'''

'''
#Comparar fitness:

poblacionPrueba = generarPoblacion()
x1 = poblacionPrueba[2]
x2 = poblacionPrueba[7]

fit1 = gte(x1, poblacionPrueba, pesos)
fit2 = gte(x2, poblacionPrueba, pesos)
ganador = compararFitness(x1, x2, poblacionPrueba)

print("Fitness x1= ", fit1, ", Fitness x2 = ", fit2)
print("El ganador es: ", poblacionPrueba.index(ganador))
'''

'''
#Mutacion y cruce:

poblacionPrueba = generarPoblacion()
x = poblacionPrueba[0]
v1 = mutacionConVecinos(x, poblacionPrueba, pesos)
print("x = ", x, ", v1 = ", v1)

y = poblacionPrueba[1]
v2 = cruce(y, poblacionPrueba, pesos, 0.3)
print("y = ", y, ", v2 = ", v2)
'''

'''
#Mejor individuo global:

diccio = {0:[(0, 4), (1, 1), (2, 5), (3, 2)], 
          1:[(0, 2), (1, 1.5), (2, 9), (3, 1.2)],
          2:[(0, 2), (1, 1.7), (2, 0.7), (3, 7)]
          }

items = diccio.items()
res = mejorIndividuoGlobal(diccio)
print(res)
'''

'''
QUEDA:
-Mostrar datos en plot
-Iterar por generaciones ***
-Memoria pdf
-Reperit todo para el segundo problema
'''