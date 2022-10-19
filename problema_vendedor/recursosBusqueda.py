#Recursos utilizados para realizar las busquedas
import sys
from collections import deque

from utils import *


class Problem:
    """The abstract class for a formal problem. You should subclass
    this and implement the methods actions and result, and possibly
    __init__, goal_test, and path_cost. Then you will create instances
    of your subclass and solve them with the various search functions."""

    def __init__(self, initial, goal=None):
        """The constructor specifies the initial state, and possibly a goal
        state, if there is a unique goal. Your subclass's constructor can add
        other arguments."""
        self.initial = initial
        self.goal = goal

    def actions(self, state):
        """Return the actions that can be executed in the given
        state. The result would typically be a list, but if there are
        many actions, consider yielding them one at a time in an
        iterator, rather than building them all at once."""
        raise NotImplementedError

    def result(self, state, action):
        """Return the state that results from executing the given
        action in the given state. The action must be one of
        self.actions(state)."""
        raise NotImplementedError

    def goal_test(self, state):
        """Return True if the state is a goal. The default method compares the
        state to self.goal or checks for state in self.goal if it is a
        list, as specified in the constructor. Override this method if
        checking against a single self.goal is not enough."""
        # if isinstance(self.goal, list):
        #     return is_in(state, self.goal)
        # else:
        #     return state == self.goal

    def path_cost(self, c, state1, action, state2):
        """Return the cost of a solution path that arrives at state2 from
        state1 via action, assuming cost c to get up to state1. If the problem
        is such that the path doesn't matter, this function will only look at
        state2. If the path does matter, it will consider c and maybe state1
        and action. The default method costs 1 for every step in the path."""
        return c + 1

    def value(self, state):
        """For optimization problems, each state has a value. Hill Climbing
        and related algorithms try to maximize this value."""
        raise NotImplementedError

# ______________________________________________________________________________

class Node:
    """A node in a search tree. Contains a pointer to the parent (the node
    that this is a successor of) and to the actual state for this node. Note
    that if a state is arrived at by two paths, then there are two nodes with
    the same state. Also includes the action that got us to this state, and
    the total path_cost (also known as g) to reach the node. Other functions
    may add an f and h value; see best_first_graph_search and astar_search for
    an explanation of how the f and h values are handled. You will not need to
    subclass this class."""

    def __init__(self, state, parent=None, action=None, path_cost=0):
        """Create a search tree Node, derived from a parent by an action."""
        self.state = state
        self.parent = parent
        self.action = action
        self.path_cost = path_cost
        self.depth = 0
        if parent:
            self.depth = parent.depth + 1

    def __repr__(self):
        return "<Node {}>".format(self.state)

    def __lt__(self, node):
        return self.state < node.state

    def expand(self, problem):
        """List the nodes reachable in one step from this node."""
        return [self.child_node(problem, action)
                for action in problem.actions(self.state)]

    def child_node(self, problem, action):
        """[Figure 3.10]"""
        next_state = problem.result(self.state, action)
        next_node = Node(next_state, self, action, problem.path_cost(self.path_cost, self.state, action, next_state))
        return next_node

    def solution(self):
        """Return the sequence of actions to go from the root to this node."""
        return [node.action for node in self.path()[1:]]

    def path(self):
        """Return a list of nodes forming the path from the root to this node."""
        node, path_back = self, []
        while node:
            path_back.append(node)
            node = node.parent
        return list(reversed(path_back))

    def __eq__(self, other):
        return isinstance(other, Node) and self.state == other.state

    def __hash__(self):
        return hash(self.state)

# ______________________________________________________________________________
# Recursos para el simulated annealing

def exp_schedule(k=20, lam=0.005, limit=100):
    """One possible schedule function for simulated annealing"""
    return lambda t: (k * np.exp(-lam * t) if t < limit else 0) 

# ---------- Minimize ---------- #
def simulated_annealing_min(problem, schedule=exp_schedule()):
    """[Figure 4.5] CAUTION: This differs from the pseudocode as it
    returns a state instead of a Node."""
    current = Node(problem.initial)
    
    print("Estado inicial: ", current.state)
    print("Valor: ", problem.value(current.state))
    
    for t in range(sys.maxsize):
        T = schedule(t)
        if T == 0:
            return current.state
        neighbors = current.expand(problem)
        if not neighbors:
            return current.state
        next_choice = random.choice(neighbors)
        delta_e = problem.value(next_choice.state) - problem.value(current.state)
        if delta_e < 0 or probability(np.exp(-delta_e / T)):
            current = next_choice

def simulated_annealing_full_min(problem, schedule=exp_schedule()):
    """ This version returns all the states encountered in reaching 
    the goal state."""
    states = []
    current = Node(problem.initial)
    
    print("Initial state: ", current.state)
    print("Value: ", problem.value(current.state))
    print()
    
    for t in range(sys.maxsize):
        states.append(current.state)
        T = schedule(t)
        if T == 0:
            return states
        neighbors = current.expand(problem)
        if not neighbors:
            return current.state
        next_choice = random.choice(neighbors)
        delta_e = problem.value(next_choice.state) - problem.value(current.state)
        if delta_e < 0 or probability(np.exp(-delta_e / T)):
            current = next_choice
            
# ---------- maximize ---------- #
def simulated_annealing_max(problem, schedule=exp_schedule()):
    """[Figure 4.5] CAUTION: This differs from the pseudocode as it
    returns a state instead of a Node."""
    current = Node(problem.initial)
    for t in range(sys.maxsize):
        T = schedule(t)
        if T == 0:
            return current.state
        neighbors = current.expand(problem)
        if not neighbors:
            return current.state
        next_choice = random.choice(neighbors)
        delta_e = problem.value(next_choice.state) - problem.value(current.state)
        if delta_e > 0 or probability(np.exp(-delta_e / T)):
            current = next_choice

def simulated_annealing_full_max(problem, schedule=exp_schedule()):
    """ This version returns all the states encountered in reaching 
    the goal state."""
    states = []
    current = Node(problem.initial)
    for t in range(sys.maxsize):
        states.append(current.state)
        T = schedule(t)
        if T == 0:
            return states
        neighbors = current.expand(problem)
        if not neighbors:
            return current.state
        next_choice = random.choice(neighbors)
        delta_e = problem.value(next_choice.state) - problem.value(current.state)
        if delta_e > 0 or probability(np.exp(-delta_e / T)):
            current = next_choice

# _____________________________________________________________________________
# Recursos utilizados para la implementacion del Genetic Algorithm

def kill(population):
    """Elimina de la población todos los individuos que no sean soluciones factibles.
    
    Args:
        population (list): lista que guarda la población.
    Returns:
        list: población con soluciones factibles.
    """    
    kill = 0
    final_population = []
    for i in population:
        p = i.copy()
        p.pop()
        for j in p:
            p.remove(j)
            if(j in p):
                kill += 1
        if kill==0:
            if(i[0] == i[len(i) - 1]):
                final_population.append(i)
    
    return final_population
            

def genetic_search(problem, ngen=1000, pmut=0.1, n=50):
    """Call genetic_algorithm on the appropriate parts of a problem.
    This requires the problem to have states that can mate and mutate,
    plus a  method that scores states."""

    # NOTE: This is not tested and might not work.
    # TODO: Use this function to make Problems work with genetic_algorithm.

    s = problem.initial
    states = [problem.result(s, a) for a in problem.actions(s)]
    random.shuffle(states)
    return genetic_algorithm(states[:n], problem.value, ngen, pmut)


def genetic_algorithm(population, fitness_fn, gene_pool, f_thres=None, ngen=1000, pmut=0.1, n=20):
    """[Figure 4.8]"""

    for i in range(ngen):
        population = [mutate_tsp(recombine(*select_tsp(2, population, fitness_fn)), pmut)
                      for i in range(len(population))]
        
        population = kill(population) # Eliminar a todos los individuos que no son soluciones.
        
        if len(population) == 1:
            print("Solo queda un individuo: ")
            return population[0]
        
        # Si pasara el caso de que terminaramos sin población,
        # se vuelve a crear una nuava población.
        if not population:
            print("Se murio toda la poblacion")
            population = init_population(n, gene_pool, len(gene_pool) + 1)
            
       
        fittest_individual = fitness_threshold(fitness_fn, f_thres, population)
        if fittest_individual:
            return fittest_individual

    # minimize
    return min(population, key=fitness_fn)


def fitness_threshold(fitness_fn, f_thres, population):
    if not f_thres:
        return None
    # minimize
    fittest_individual = min(population, key=fitness_fn)
    if fitness_fn(fittest_individual) <= f_thres:
        return fittest_individual

    return None


def init_population(pop_number, gene_pool, state_length):
    """Initializes population for genetic algorithm
    pop_number  :  Number of individuals in population
    gene_pool   :  List of possible values for individuals
    state_length:  The length of each individual"""
    
    population = []
    
    for i in range(pop_number):
        state = []
        genes = gene_pool.copy()
        for j in range(len(genes)):
            g = random.randrange(0, len(genes))
            state.append(genes[g])
            genes.remove(genes[g])
        state.append(state[0])
        population.append(state)
    return population
        

#Funcion mediante la cual obtenemos a los padres para la reproduccion escogiendo a los individuos que tengan un fitness 
#menor o igual a la media
def select_tsp(r, population, fitness_fn):
    fitnesses = list(map(fitness_fn, population))
    print("population: ", population)
    print(fitnesses)
    med = 0
    for i in fitnesses:
        med += i  
    
    med = med / len(population)
    
    seq = []
    i = 0
    while(len(seq) < r and len(fitnesses) > i):
        if(fitnesses[i] <= med):
            seq.append(population[i])
        i+=1
    return seq
    
 #Reproduccion de los padres   
def recombine(x, y=None):
    if(not y):
        return x
    
    n = len(x)
    c = random.randrange(0, n)
    r = x[:c] + y[c:]
    r[n - 1] = r[0]
    return r


def recombine_uniform(x, y):
    n = len(x)
    result = [0] * n
    indexes = random.sample(range(n), n)
    for i in range(n):
        ix = indexes[i]
        result[ix] = x[ix] if i < n / 2 else y[ix]

    return ''.join(str(r) for r in result)

# mutamos a los individuos intercambiando dos genes de un estado
def mutate_tsp(x ,pmut):
    if random.uniform(0, 1) >= pmut:
        return x
    
    mutated_state = x.copy()
    l = len(x) - 1
    i = random.randrange(0, (l))
    j = random.randrange(0, (l))
    while (j == i):
        j = random.randrange(0, (l))
                
    city_1 = x[i]
    city_2 = x[j]

    mutated_state[i] = city_2
    mutated_state[j] = city_1

    mutated_state[l] = mutated_state[0]
    return mutated_state
    

# _____________________________________________________________________________
