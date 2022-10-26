from cmath import pi, sin, sqrt
import operator
import numpy
import random


#------------------------------------------------INICIALIZACION--------------------------------------------------------

pesos = [
    (0.9,0.1),
    (0.8,0.2),
    (0.7,0.3),
    (0.95,0.05),
    (0.96,0.04),
    (0.75,0.25),
    (0.85,0.15),
    (0.67,0.33),
    (0.79,0.21),
    (0.91,0.09),
    (0.95,0.05),
    (0.88,0.12),
    (0.74,0.26),
    (0.57,0.43),
    (0.92,0.08),
    (0.99,0.01),
    (0.77,0.23),
    (0.71,0.29),
    (0.6,0.4),
    (0.55,0.45)
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

def evaluarGeneracionF1F2(poblacion):        #Obtenemos una lista ordenada por el indice del individuo
    lista = []
    for i in range(len(poblacion)):
        x = poblacion[i]
        f1 = x[0]
        f2 = funcionF2(x)
        media = (f1 + f2)/2
        lista.append((i, f1, f2, media))
    listaFinal = sorted(lista, key=lambda x:x[3])
    return listaFinal

def compararFitness(x, y, poblacion, i):
    fit1 = gte(x, poblacion, pesos, i)
    fit2 = gte(y, poblacion, pesos, i)
    if fit1 < fit2:
        return x
    else: 
        return y

def compararF1F2(x, y, poblacion, i):
    f1x = x[0]
    f1y = y[0]
    f2x = funcionF2(x)
    f2y = funcionF2(y)

    if (f1x > f1y) and (f2x < f2y):
        return x
    elif (f1y > f1x) and (f2y < f2x):
        return y
    else:
        return compararFitness(x, y, poblacion, i)
        
#-----------------------------------------------------------------CRUCE Y MUTACION-----------------------------------------------------------------

def mutacionConVecinos(x, poblacion, pesos, numVecinos):
    indiceX = poblacion.index(x)
    pesoX = pesos[indiceX]                         #Obtenemos la vecindad completa de un individuo
    vecinosX = obtenerVecinos(pesoX, numVecinos)            #NumVecinos = 3   
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
    
def cruce1(x, poblacion, pesos, probabilidad, numVecinos):     
    v = mutacionConVecinos(x, poblacion, pesos, numVecinos)
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

#--------------------------------------------OPERACIONES EN FICHERO-------------------------------------------------------

def escribirMejoresMetricas(registroFitness, registroF1F2, generacion):
    mejorFitness = registroFitness[generacion]
    mejorF1F2 = registroF1F2[generacion]
    s1 = str("-Generacion Nº " + str(generacion) + '\n')
    s2 = str("Mejor Fitness de la Generacion = " + str(mejorFitness[0][1]) + " // Individuo: " + str(mejorFitness[0][0]) + '\n')
    s3 = str("Mejores F1F2 = " + str(mejorF1F2[0][1]) + ', ' + str(mejorF1F2[0][2]) + " // Individuo: " + str(mejorF1F2[0][0]) + '\n')
    s4 =('----------------------------------------------------------------------------------------------\n')
    return s1 + s2 + s3 + s4
    
def obtenerPuntosFrente(fichero = 'documentos/pareto.txt'):
    x = []
    y = []
    with open(fichero, 'r', encoding = 'utf-8') as f:
        for linea in f:
            arrayAux = linea.split('\t')
            f1 = float(arrayAux[0])
            f2aux = arrayAux[-1].replace("\n", '')
            f2 = float(f2aux)
            x.append(f1)
            y.append(f2)
        f.close()
    return [x, y]    

def obtenerPuntosGeneracion(registroF1F2, generacion):
    x = []
    y = []
    poblacion = registroF1F2[generacion]
    for individuo in poblacion:
        x.append(individuo[1])
        y.append(individuo[2])
    return [x, y]

def obtenerPuntosTotales(registroF1F2):
    x = []
    y = []
    for i in range(len(list(registroF1F2.items()))):
        puntosi = obtenerPuntosGeneracion(registroF1F2, i)
        xi = puntosi[0]
        yi = puntosi[1]
        x = x + xi
        y = y + yi
    return [x, y]

def obtenerPuntosZDT3(fichero):
    x = []
    y = []
    with open(fichero, 'r', encoding = 'utf-8') as f:
        for linea in f:
            arrayAux = linea.split('\t')
            f1 = float(arrayAux[0])
            f2aux = arrayAux[1]
            f2 = float(f2aux)
            x.append(f1)
            y.append(f2)
        f.close()
    return [x, y] 
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
#Escritura en fichero:

poblacion = generarPoblacion(20)
poblacion2 = []
probCruce = 0.6

registroFitness = {}
registroF1F2 = {}

registroFitness[0] = evaluarGeneracion(poblacion, pesos)
registroF1F2[0] = evaluarGeneracionF1F2(poblacion)

for i in range(len(poblacion)):
    p = random.random()
    x = poblacion[i]
    xm = cruce1(x, poblacion, pesos, probCruce)             
    y = compararFitness(x, xm, pesos, i)                    
    poblacion2.append(y)

registroFitness[1] = evaluarGeneracion(poblacion2, pesos)
registroF1F2[1] = evaluarGeneracionF1F2(poblacion2)

string = ''
for j in range(len(registroFitness.items())):
    string = string + escribirMetricas(registroFitness, registroF1F2, j)

with open('metricas.txt', 'w', encoding = 'utf-8') as f:
    f.write(string)
    f.close()
'''

'''
#Obtener frente:

puntos = obtenerPuntosFrente()
print(puntos)
'''

'''
QUEDA:
-Mostrar datos en plot
-Memoria pdf
-Reperit todo para el segundo problema
'''