from recursosBusqueda import *

class JugProblem(Problem):
    def __init__(self, initial, goal):
        super().__init__(initial, goal)
    
    def actions(self, state):
        actions_lsit = []
        
        if(state[0] > 0):
            actions_lsit.append("vaciar12")
        if(state[1] > 0):
            actions_lsit.append("vaciar8")
        if(state[2] > 0):
            actions_lsit.append("vaciar3")
            
        if(state[0] < 12):
            actions_lsit.append("llenar12")
        if(state[1] < 8):
            actions_lsit.append("llenar8")
        if(state[2] < 3):
            actions_lsit.append("llenar3")
            
        if(state[0] > 0 and state[1] < 8):
            actions_lsit.append("de12a8")
        if(state[0] > 0 and state[2] < 3):
            actions_lsit.append("de12a3")
            
        if(state[1] > 0 and state[0] < 12):
            actions_lsit.append("de8a12")
        if(state[1] > 0 and state[2] < 3):
            actions_lsit.append("de8a3")
            
        if(state[2] > 0 and state[0] < 12):
            actions_lsit.append("de3a12")
        if(state[2] > 0 and state[1] < 8):
            actions_lsit.append("de3a8")
            
        return actions_lsit

    def result(self, state, action):
        x, y, z = state[0], state[1], state[2]
        #Vaciar
        if(action == "vaciar12"):
            x = 0
        elif(action == "vaciar8"):
            y = 0
        elif(action == "vaciar3"):
            z = 0
        #Llenar
        if(action == "llenar12"):
            x = 12
        elif(action == "llenar8"):
            y = 8
        elif(action == "llenar3"):
            z = 3
        #Verter desde 12 
        if(action == "de12a8"):
            L = 8 - y
            if (L < x):
                x = x - L
                y = y + L
            elif (L >= x):
                y = y + x
                x = 0
        if(action == "de12a3"):
            L = 3 - z
            if (L < x):
                x = x - L
                z = z + L
            elif (L >= x):
                z = z + x
                x = 0
        #Verter desde 8 
        if(action == "de8a12"):
            L = 12 - x
            if (L < y):
                y = y - L
                x = x + L
            elif (L >= y):
                x = x + y
                y = 0
        if(action == "de8a3"):
            L = 3 - z
            if (L < y):
                y = y - L
                z = z + L
            elif (L >= y):
                z = z + y
                y = 0
        #Verter desde 3
        if(action == "de3a12"):
            L = 12 - x
            if (L < z):
                z = z - L
                x = x + L
            elif(L >= z):
                x = x + z
                z = 0
        if(action == "de3a8"):
            L = 8 - y
            if (L < z):
                z = z - L
                y = y + L
            elif (L >= z):
                y = y + z
                z = 0
        
        return (x, y, z)
    
    def goal_test(self, state):
        return (self.goal in state)

pJarras = JugProblem((0,0,0), 1)

nodo = breadth_first_graph_search(pJarras)

if nodo:
    print(nodo.path())
    print(nodo.solution())
else:
    print("No hay solucion")


