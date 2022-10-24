import funciones

lista1 = [1, 2, 5, 6, 4]
lista2 = [9, 3, 7, 3, 8]
print(lista1, lista2)
lista2 = lista1.copy()
print(lista2)
lista2[0] = 0
print(lista1, lista2)



lista1 = [(0,5), (1, 4), (2, 1), (3, 2)]
maximo = max(lista1, key = lambda x: x[1])
print(maximo)


diccio = {0:[(0, 4), (1, 1), (2, 5), (3, 2)], 
          1:[(0, 2), (1, 1.5), (2, 9), (3, 1.2)],
          2:[(0, 2), (1, 1.7), (2, 0.7), (3, 7)]
          }

items = diccio.items()
res = funciones.mejorIndividuoGlobal(diccio)
print(diccio[1])
print(res)