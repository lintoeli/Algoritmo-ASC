import random
import funciones

#-------------------------------------------INICIALIZACION------------------------------------------------------

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
 
poblacionInicial = funciones.generarPoblacion()   #Servira para comparar con los fitness finales
poblacion = poblacionInicial.copy()
print(poblacion)
generaciones = 500
probCruce = 0.5
registroGeneraciones = {}                         #Estos registros facilitaran la muestra de datos posteriormente
registroFitnessPorGeneracion = {}
registroF1F2PorGeneracion = {}

#-------------------------------------------PROCEDIMIENTO------------------------------------------------------------

for i in range(generaciones):
    registroGeneraciones[i] = poblacion                                     #Comenzamos guardando en el registro
    nextGen = []                                                            #los individuos de la presente generacion
    for j in range(len(poblacion)):
        p = random.random()
        x = poblacion[j]                                                    #Generamos un nuevo individuo mediante
        xm = funciones.cruce1(x, poblacion, pesos, probCruce)               #cruce y mutacion, y nos quedamos con el
        y = funciones.compararFitness(x, xm, pesos, j)                      #mejor entre el nuevo y el original
        nextGen.append(y)
    fitnessGeneracion = funciones.evaluarGeneracion(poblacion, pesos)       #Una vez terminados todos los cruces y
    registroFitnessPorGeneracion[i] = fitnessGeneracion
    f1f2 = funciones.evaluarGeneracionF1F2(poblacion)
    registroF1F2PorGeneracion[i] = f1f2                                     #mutaciones, la nueva poblacion con la que
    poblacion = nextGen.copy()                                              #trabajar pasa a ser la lista nextGen para
    print("Comenzando generación ", i+1)                                    #la siguiente iteracion

print("Última generacion: ", poblacion)
print("Fitness iniciales: ", funciones.evaluarGeneracion(poblacionInicial, pesos))
print("Fitness finales: ", funciones.evaluarGeneracion(poblacion, pesos))
print("F1 // F2 iniciales: ", registroF1F2PorGeneracion[0])
print("F1 // F2 finales: ", registroF1F2PorGeneracion[generaciones - 1])
                                                                            


                                                            
    
