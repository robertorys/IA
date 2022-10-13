from Nodo import Nodo

# Constantes que guardan la capacidad de cada jarrón
Cx = 12
Cy = 8
Cz = 3

# Función que pasa el agua de una jarra a otra
# Regresa un arreglo donde array[0] es el que paso agua y array[1] el que recibió agua
def deXaY(x, y, Cy):
    Ly = Cy - y
    
    if (Ly < x):
        x = x - Ly
        y = y + Ly
        return x, y
    elif (Ly >= x):
        y = y + x
        return 0, y
        

# Función que realiza la busqueda de la solución con un método de busqueda por anchura
def buscar_solucion(estado_inicial, solucion):
    solucion_flag = False # Bandera para determinar si se encontró la solución
    nodos_visitados = [] # Arreglo de los nodos visitados
    nodos_frontera = [] # Arreglo de los nodos en la frontera
    
    path_nodo = []
    
    nodoInicial = Nodo(estado_inicial) # Crear el nodo del estado inicial
    nodos_frontera.append(nodoInicial) # Agreegar el estado inicial a al frontera
    
    # Bucle while que generara y buscara los estados que lleven a la solución
    # Mientras la bandera de la solución no pase a True y el arreglo de nodos de frontera no sea 0 se repetira
    while ((not solucion_flag) and (len(nodos_frontera) != 0)):
        nodo = nodos_frontera.pop(0) # Extraer nodo a visitar
        nodos_visitados.append(nodo) # Añadir a nodos visitados
        
        # Si en el nodo de un jarrón tiene 1, ya sea en x, y, ó z, encontró la solucón
        for n in nodo.get_datos(): 
            if n == 1:
                solucion_flag = True
                return nodo # Devuelve el nodo meta
        
        # Si no se encuentra la solución se expanden los hijos
        dato_nodo = nodo.get_datos()
        
        # Llenar jarras
        # Llenar grande
        hijo = [Cx, dato_nodo[1], dato_nodo[2]]
        hijo_1 = Nodo(hijo) # Creación de nodo hijo
        
        # Agreagar a la frontera si no se a creado un estado igaul en la frontera o en visitados
        if not hijo_1.en_lista(nodos_visitados) and not hijo_1.en_lista(nodos_frontera):
            nodos_frontera.append(hijo_1)
        
        # Llenar mediana
        hijo = [dato_nodo[0], Cy, dato_nodo[2]]
        hijo_2 = Nodo(hijo)
        
        if not hijo_2.en_lista(nodos_visitados) and not hijo_2.en_lista(nodos_frontera):
            nodos_frontera.append(hijo_2)

        # Llenar pequeña
        hijo = [dato_nodo[0], dato_nodo[1], Cz]
        hijo_3 = Nodo(hijo)
        
        if not hijo_3.en_lista(nodos_visitados) and not hijo_3.en_lista(nodos_frontera):
            nodos_frontera.append(hijo_3)
        
        # Vaciar jarras
        # Vaciar grande
        hijo = [0, dato_nodo[1], dato_nodo[2]]
        hijo_4 = Nodo(hijo)
        
        if not hijo_4.en_lista(nodos_visitados) and not hijo_4.en_lista(nodos_frontera):
            nodos_frontera.append(hijo_4)
        
        # Vaciar mediana
        hijo = [dato_nodo[0], 0, dato_nodo[2]]
        hijo_5 = Nodo(hijo)
        
        if not hijo_5.en_lista(nodos_visitados) and not hijo_5.en_lista(nodos_frontera):
            nodos_frontera.append(hijo_5)

        # Vaciar pequeña
        hijo = [dato_nodo[0], dato_nodo[1], 0]
        hijo_6 = Nodo(hijo)
        
        if not hijo_6.en_lista(nodos_visitados) and not hijo_6.en_lista(nodos_frontera):
            nodos_frontera.append(hijo_6)
                
        # Transportar de un jarrón a otro
        # Transportar grande-mediano x -> y
        regreso = deXaY(dato_nodo[0], dato_nodo[1], Cy) # Regresa un arreglo donde regreso[0] es el que pasa y regreso[1] el que resibe
        hijo = [regreso[0], regreso[1], dato_nodo[2]]
        hijo_7 = Nodo(hijo)
        
        if not hijo_7.en_lista(nodos_visitados) and not hijo_7.en_lista(nodos_frontera):
            nodos_frontera.append(hijo_7)
        
        # Transportar grande-pequeña x -> z
        regreso = deXaY(dato_nodo[0], dato_nodo[2], Cz)
        hijo = [regreso[0], dato_nodo[1], regreso[1]]
        hijo_8 = Nodo(hijo)
        
        if not hijo_8.en_lista(nodos_visitados) and not hijo_8.en_lista(nodos_frontera):
            nodos_frontera.append(hijo_8)
        
        # Transportar mediano-grande y -> x
        regreso = deXaY(dato_nodo[1], dato_nodo[0], Cx)
        hijo = [regreso[1], regreso[0], dato_nodo[2]]
        hijo_9 = Nodo(hijo)
        
        if not hijo_9.en_lista(nodos_visitados) and not hijo_9.en_lista(nodos_frontera):
            nodos_frontera.append(hijo_9)
        
        # Transportar mediano-pequeño y -> z
        regreso = deXaY(dato_nodo[1], dato_nodo[2], Cz)
        hijo = [dato_nodo[0], regreso[0], regreso[1]]
        hijo_10 = Nodo(hijo)
        
        if not hijo_10.en_lista(nodos_visitados) and not hijo_10.en_lista(nodos_frontera):
            nodos_frontera.append(hijo_10)
                    
        # Transportar pequeño-grande z -> x
        regreso = deXaY(dato_nodo[2], dato_nodo[0], Cx)
        hijo = [regreso[1], dato_nodo[1], regreso[0]]
        hijo_11 = Nodo(hijo)
        
        if not hijo_11.en_lista(nodos_visitados) and not hijo_11.en_lista(nodos_frontera):
            nodos_frontera.append(hijo_11)
                    
        # Transportar pequeño-mediano z -> y
        regreso = deXaY(dato_nodo[2], dato_nodo[1], Cy)
        hijo = [dato_nodo[0], regreso[1], regreso[0]]
        hijo_12 = Nodo(hijo)
        
        if not hijo_12.en_lista(nodos_visitados) and not hijo_12.en_lista(nodos_frontera):
            nodos_frontera.append(hijo_12)
        
        # Agregar los nodos hijos al padre
        nodo.set_hijos([hijo_1, hijo_2, hijo_3, hijo_4, hijo_5, hijo_6, hijo_7, hijo_8, hijo_9, hijo_9, hijo_10, hijo_11, hijo_12])       
                      
# Función main
def main():
    estado_inicial = [0, 0, 0]
    solucion = 1
    
    # Buscar la sulución por busqueda en anchura
    nodo_solucion = buscar_solucion(estado_inicial, solucion)
    
    # Creo una lista donde van todos los padres del nodo solución
    resultado = []
    nodo = nodo_solucion

    # Reocre de nodo padre en nodo padre desde el nodo solución
    while nodo.get_padre() != None:
        resultado.append(nodo.get_datos())
        nodo = nodo.get_padre()
 
    resultado.append(estado_inicial) # Agrega nodo solcuión al final del arreglo
    resultado.reverse() # Invierte las posiciones del arreglo para leer la solución de pare a hijo
 
    print(resultado)
    
main()


