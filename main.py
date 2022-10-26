import random
import funciones
import matplotlib.pyplot as plt

#-------------------------------------------INICIALIZACION------------------------------------------------------

pesos = [                               #Siempre en paquetes de 20
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

pesos = pesos * 1                                 #Modificador cantidad de individuos


generaciones = int(10000/len(pesos))              #Parametros a establecer
probCruce = 0.5
numVecinos = int(3)                                 #Tamaño de la vecindad = 3 (funciona mejor que el 10-30%)

poblacionInicial = funciones.generarPoblacion()   #Servira para comparar con los fitness finales
poblacion = poblacionInicial.copy()

registroGeneraciones = {}                         #Estos registros facilitaran la muestra de datos posteriormente
registroFitnessPorGeneracion = {}
registroF1F2PorGeneracion = {}

cadena = ''                                       #String que recogera los datos generacion por generacion

#-------------------------------------------PROCEDIMIENTO------------------------------------------------------------

for i in range(generaciones):
    registroGeneraciones[i] = poblacion                                     #Comenzamos guardando en el registro
    nextGen = []                                                            #los individuos de la presente generacion
    for j in range(len(poblacion)):
        p = random.random()
        x = poblacion[j]                                                    #Generamos un nuevo individuo mediante
        xm = funciones.cruce1(x, poblacion, pesos, probCruce, numVecinos)               #cruce y mutacion, y nos quedamos con el
        y = funciones.compararF1F2(x, xm, pesos, j)                         #mejor entre el nuevo y el original
        nextGen.append(y)
    fitnessGeneracion = funciones.evaluarGeneracion(poblacion, pesos)       #Una vez terminados todos los cruces y
    registroFitnessPorGeneracion[i] = fitnessGeneracion                     #mutaciones, la nueva poblacion con la que
    f1f2 = funciones.evaluarGeneracionF1F2(poblacion)                       #trabajar pasa a ser la lista nextGen para
    registroF1F2PorGeneracion[i] = f1f2                                     #la siguiente iteracion
    poblacion = nextGen.copy()                                              
    print("Comenzando generación ", i+1)
    cadena = cadena + funciones.escribirMejoresMetricas(registroFitnessPorGeneracion, registroF1F2PorGeneracion, i)                                    

#-------------------------------------------INTERPRETACION DE DATOS----------------------------------------------------------

with open('documentos/resultado.txt', 'w', encoding = 'utf-8') as f:                    #Escribir en el fichero
    f.write(cadena)
    f.close()

puntosFrente = funciones.obtenerPuntosFrente()                                          #Obtenemos el frente de Pareto
frenteX = puntosFrente[0]                                                               #ideal
frenteY = puntosFrente[1]

puntosIndividuosFinales = funciones.obtenerPuntosGeneracion(registroF1F2PorGeneracion, generaciones - 1)
individuosX = puntosIndividuosFinales[0]                                                #Obtenemos los valores de f1 y f2
individuosY = puntosIndividuosFinales[1]                                                #de los individuos de la ultima
                                                                                        #generacion
plt.scatter(frenteX, frenteY, s = 6)
plt.scatter(individuosX, individuosY, s = 5, color = 'black')                 #Construimos la grafica
plt.margins(0.1)
plt.xlabel("f1")    
plt.ylabel("f2")                                                  
plt.show()

                                                            
    
