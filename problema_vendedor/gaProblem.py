import csv
import random

from recursosBusqueda import *


class tspag(Problem):
    def __init__(self, initial, matrix, goal=None):
        self.matrix = matrix
        super().__init__(initial, goal)

    def actions(self, state):
        actions = "new_state"
        return actions

    def result(self, state, action):
        # Crea un nuevo estado aleatorio
        newState = []
        genes = tGenes()
        if (action == "new_state"):
            for j in range(len(genes)):
                g = random.randint(0, len(genes) - 1)
                newState.append(genes[g])
                genes.remove(genes[g])
            newState.append(newState[0])

        return newState

    # Función objetivo.
    def value(self, state):
        fitness = 0
        for i in range(len(state) - 1):
            fitness += matrix[state[i]][state[i+1]]
        return fitness

# Leer la matriz de distancias desde un archivo csv
def readcsvm():
    matrix, a, b = [], [], []
    with open('a.csv') as csvfile:
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
                i += 1          
        csvfile.close()
    return matrix

matrix = readcsvm()


# Obtiene todas las ciudades para usarlas como genes
def tGenes():
    genes = []
    n = 0
    with open('a.csv') as csvfile:
        csvreader = csv.reader(csvfile, delimiter=",")
        for i in csvreader:
            n += 1
    for i in range(n - 1):
        genes.append(i)
    return genes
# Tododo los genes
genes = tGenes()
# Copia de los genes
genesc = genes.copy()

# Generar un estado inicial aleatorio.
state = []

for g in range(len(genesc)):
    i = random.randrange(0, len(genesc))
    state.append(genesc[i])
    genesc.remove(genesc[i])
state.append(state[0])

# Creación del problema del viajero con las especificaciones para el algoritmo genético.
# No es necesario crear en la clase del problema una manera de saber si una solución es factible, 
# ya que se hacen las restricciones en el algoritmo genético.
tsp = tspag(state, matrix)

def genetic_search_i(problem, genes, ng=20, pmut=0.5, n=20):
    """Llame al genetic_algorithm en las partes apropiadas de un problema. 
    Esto requiere que el problema tenga estados que puedan emparejarse y mutar,
    además de un método de value que puntúe los estados."""
    
    states = []
    states = init_population(n, genes, len(problem.initial))
    states.append(problem.initial)

    # llama a genetic_algorithm.
    # Tiene como argumentos: 
    # la población creada, la función objetivo,los genes del problema, ng generaciones y la probabilidad de mutación
    return genetic_algorithm(states[:n], problem.value, gene_pool=genes, ngen=ng, pmut=pmut, n=n)

state = genetic_search_i(tsp, genes)

if state:
    fitness = 0        
    for i in range(len(state) - 1):
        fitness += matrix[state[i]][state[i+1]]

    print("Solucion encontrada: ", state)
    print("valor = ", fitness)


