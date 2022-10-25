import random
import string
import funciones

#-------------------------------------------INICIALIZACION------------------------------------------------------

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
 
poblacionInicial = funciones.generarPoblacion()   #Servira para comparar con los fitness finales
poblacion = poblacionInicial.copy()
print(poblacion)
generaciones = 500
probCruce = 0.5
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
        xm = funciones.cruce1(x, poblacion, pesos, probCruce)               #cruce y mutacion, y nos quedamos con el
        y = funciones.compararF1F2(x, xm, pesos, j)                         #mejor entre el nuevo y el original
        nextGen.append(y)
    fitnessGeneracion = funciones.evaluarGeneracion(poblacion, pesos)       #Una vez terminados todos los cruces y
    registroFitnessPorGeneracion[i] = fitnessGeneracion                     #mutaciones, la nueva poblacion con la que
    f1f2 = funciones.evaluarGeneracionF1F2(poblacion)                       #trabajar pasa a ser la lista nextGen para
    registroF1F2PorGeneracion[i] = f1f2                                     #la siguiente iteracion
    poblacion = nextGen.copy()                                              
    print("Comenzando generación ", i+1)
    cadena = cadena + funciones.escribirMejoresMetricas(registroFitnessPorGeneracion, registroF1F2PorGeneracion, i)                                    
'''
print("Última generacion: ", poblacion)
print("Fitness iniciales: ", funciones.evaluarGeneracion(poblacionInicial, pesos))
print("Fitness finales: ", funciones.evaluarGeneracion(poblacion, pesos))
print("F1 // F2 iniciales: ", registroF1F2PorGeneracion[0])
print("F1 // F2 finales: ", registroF1F2PorGeneracion[generaciones - 1])
'''

with open('documentos/mejoresMetricas.txt', 'w', encoding = 'utf-8') as f:                    #Escribir en el fichero
    f.write(cadena)
    f.close()
                                                                            


                                                            
    
