import csv

from recursosBusqueda import *


class tspsa(Problem):
    def __init__(self, initial, matrix, goal=None):
        self.matriz = matrix
        super().__init__(initial, goal)  
     
    def actions(self, state):
        return ["vecino"]
        
    def result(self, state, action):
        """Método para determinar un vecino"""
        next_state = []
        next_state = state.copy()
        if (action == "vecino"):
            i = random.randrange(0, len(state) - 1)
            j = random.randrange(0, len(state) - 1)
            while (i == j):
                j = random.randrange(0, len(state) - 1)
            
            city_1 = state[i]
            city_2 = state[j]
            
            next_state[i] = city_2
            next_state[j] = city_1
            next_state[len(next_state) - 1] = next_state[0]

        return next_state
    
    # Función a optimizar          
    def value(self, state):
        total=0
        for i in range(len(state) - 1):
            total += self.matriz[state[i]][state[i+1]]
        
        return total

# Leer la matriz desde un archivo csv
def readcsvm():
    matrix, a, b = [], [], []
    with open('10c.csv') as csvfile:
        csvreader = csv.reader(csvfile, delimiter=",")
        i = 0
        for line in csvreader:
            if i > 0:
                a = line[1:]
                for c in a:
                    b.append(int(c))
                matrix.append(b.copy())
                b.clear()
                a.clear() 
            else:
                   i+=1 
        csvfile.close()
    return matrix

# Matriz que guarda la longitud de los caminos entre ciudades.
matrix = readcsvm()

# Arreglo que guarda todas las ciudades
totalCiudades = []

for i in range (len(matrix)):
    totalCiudades.append(i)
    

# Crear un estado aleatorio
def init_state(ciudades):
    c = []
    l = len(ciudades)
    for i in range(l):
        j = random.randrange(0, len(ciudades))
        c.append(ciudades[j])
        ciudades.remove(ciudades[j])
    c.append(c[0])
    return c

def linear_schedule(k=10, T=1000, limit=100):
    """Comportamiento lineal para la temperatura."""
    return lambda t: (-(k * t) + T) if t < limit else 0

def val(state):
    """Evaluar el valor de un estado regresado por el algoritmo."""
    total = 0
    for i in range(len(state) - 1):
        total += matrix[state[i]][state[i+1]]
    return total

def p_simulated_annealing_n(n): 
    """Repetir n-veces el algoritmo."""
    for i in range(n):
        state = init_state(totalCiudades.copy())
        tsp = tspsa(state, matrix , 0) # Crear el problema con el estado inicial, es un estado aleatorio.
        print("Prueba ", i+1, ":")
        # linear_schedule(k=pendiente, T=temperatura inicial, limit=iteración donde regresa negativo)
        sol = simulated_annealing_min(tsp, linear_schedule(k=10, T=100000, limit=10000))
        v = val(sol)
        print("Estado final: ", sol)
        print("Valor: ", v)
        print()

def p_simulated_annealing_full():
    """Regresa los todos los estados que ha visitado."""
    tsp = tspsa(init_state(totalCiudades.copy()), matrix , 0) # Crear el problema con el estado inicial.
    path = simulated_annealing_full_min(tsp, linear_schedule())
    print(path)
    sol = path[len(path) - 1]
    
    v = val(sol)
    print("Estado final: ", sol)
    print("Valor: ", v)
    print()
   
n = 1
p_simulated_annealing_n(n)
# p_simulated_annealing_full()
