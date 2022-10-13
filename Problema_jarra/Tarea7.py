'''
Problema 
You have three jugs, measuring 12 gallons, 8 gallons, and 3 gallons,
and a water faucet. You can fill the jugs up or empty them out from one to
another or onto the ground. You need to measure out exactly one gallon.
Estado Inicial: (0,0,0)
Estados: Tripleta de gallones(0,0,0),...,(12,8,3)
Objetivo: Alguna jarra con 1 galon (1,*,*),(*,1,*),(*,*,1)
Modelo de transicion: Definir cada estado en un grafo y la accion 
te lleva al siguiente nodo
Prueba de Objetivo:Alguna de las 3 variables ya contiene el 1?
Costo del camino: Cada accion equivale a 1 unidad de costo el mejor 
camino es el de menor costo
'''

from collections import deque
from recursosBusqueda import *


#Metas se puede definir como una condicional

class ProblemaJarras(Problem):
    def __init__(self, initial, goal=None,limits=None):
        super().__init__(initial, goal)
        self.limits=limits
        

    def actions(self,state):
        result_actions=[]
        #Lista para todas las acciones posibles
        #Si se puede llenar la jarra
        J1,J2,J0=False,False,False
        if state[0]<self.limits[0]:
            result_actions.append("Llenar Primera Jarra")
            J0=True
        if state[1]<self.limits[1]:
            result_actions.append("Llenar Segunda Jarra")
            J1=True
        if state[2]<self.limits[2]:
            result_actions.append("Llenar Tercera Jarra")
            J2=True
        #Si la primera jarra tiene agua para verter
        if state[0]>0:
            result_actions.append("Vaciar Primera Jarra")
            #Si la segunda jarra tiene espacio para verter
            if J1:
                result_actions.append("Verter 0-1")
            if J2:
                result_actions.append("Verter 0-2")
        #Si la segunda jarra tiene agua para verter
        if state[1]>0:
            result_actions.append("Vaciar Segunda Jarra")
            if J0:
                result_actions.append("Verter 1-0")
            if J2:
                result_actions.append("Verter 1-2")
        if state[2]>0:
            result_actions.append("Vaciar Tercera Jarra")
            if J0:
                result_actions.append("Verter 2-0")
            if J1:
                result_actions.append("Verter 2-1")
        print(f"result_actions= {result_actions}")
        return result_actions
        
    def result(self, state, action):
        #Llenar
        if action=="Llenar Primera Jarra":
            res=(self.limits[0],state[1],state[2])
        if action=="Llenar Segunda Jarra":
            res=(state[0],self.limits[1],state[2])
        if action=="Llenar Tercera Jarra":
            res=(state[0],state[1],self.limits[2])
        #Vaciar
        if action=="Vaciar Primera Jarra":
            res=(0,state[1],state[2])
        if action=="Vaciar Segunda Jarra":
            res=(state[0],0,state[2])
        if action=="Vaciar Tercera Jarra":
            res=(state[0],state[1],0)
        #Verter Desde 0
        cap_act=state[0]
        if action=="Verter 0-1":
            cap_ver=self.limits[1]-state[1]
            if cap_act>cap_ver:
                res=(state[0]-cap_ver,self.limits[1],state[2])
            else:
                res=(0,state[1]+cap_act,state[2])
        if action=="Verter 0-2":
            cap_ver=self.limits[2]-state[2]
            if cap_act>cap_ver:
                res=(state[0]-cap_ver,state[1],self.limits[2])
            else:
                res=(0,state[1],state[2]+cap_act)
        
        #Verter Desde 1
        cap_act=state[1]
        if action=="Verter 1-0":
            cap_ver=self.limits[0]-state[0]
            if cap_act>cap_ver:
                res=(self.limits[0],state[1]-cap_ver,state[2])
            else:
                res=(state[0]+cap_act,0,state[2])
        if action=="Verter 1-2":
            cap_ver=self.limits[2]-state[2]
            if cap_act>cap_ver:
                res=(state[0],state[1]-cap_ver,self.limits[2])
            else:
                res=(state[0],0,state[2]+cap_act)
        #Verter Desde 2
        cap_act=state[2]
        if action=="Verter 2-0":
            cap_ver=self.limits[0]-state[0]
            if cap_act>cap_ver:
                res=(self.limits[0],state[1],state[2]-cap_ver)
            else:
                res=(state[0]+cap_act,state[1],0)
        if action=="Verter 2-1":
            cap_ver=self.limits[1]-state[1]
            if cap_act>cap_ver:
                res=(state[0],self.limits[1],state[2]-cap_ver)
            else:
                res=(state[0],state[1]+cap_act,0)
        #Return
        return res

    def goal_test(self, state):
        if state[0]==1 or state[1]==1 or state[2]==1:
            return True
        else:
            return False

Jarritas=ProblemaJarras((0,0,0),limits=(12,8,3))

def breadth_first_search_graph(problem):
    "[Figure 3.11]"
    
    # we use these two variables at the time of visualisations
    iterations = 0
    #all_node_colors = []
    #node_colors = {k : 'white' for k in problem.graph.nodes()}
    
    node = Node(problem.initial)
    print(f"Nodo inicial {node}")
    #node_colors[node.state] = "red"
    iterations += 1
    #all_node_colors.append(dict(node_colors))
      
    if problem.goal_test(node.state):
        #node_colors[node.state] = "green"
        iterations += 1
        #all_node_colors.append(dict(node_colors))
        return(iterations, node)
    
    frontier = deque([node])
    print(f"frontier = {frontier}")
    # modify the color of frontier nodes to blue
    #node_colors[node.state] = "orange"
    iterations += 1
    #all_node_colors.append(dict(node_colors))
        
    explored = set()
    while frontier:
        node = frontier.popleft()
        
        #node_colors[node.state] = "red"
        iterations += 1
        #all_node_colors.append(dict(node_colors))
        
        explored.add(node.state)     
        print(f"node= {node}, frontier={frontier}\n explored={explored}\n iteration={iterations}")
        for child in node.expand(problem):
            #print("Expandiendo a nodos hijos")
            if child.state not in explored and child not in frontier:
                #print("El estado no esta explorado ni en frontera")
                if problem.goal_test(child.state):
                    #print("El nodo es el objetivo")
                    #node_colors[child.state] = "green"
                    iterations += 1
                    #all_node_colors.append(dict(node_colors))
                    return(iterations, child)
                frontier.append(child)
                #print("Agrega al hijo a la frontera y aumenta la iteracion")
                #node_colors[child.state] = "orange"
                iterations += 1
                #all_node_colors.append(dict(node_colors))
        #node_colors[node.state] = "gray"
        iterations += 1
        #all_node_colors.append(dict(node_colors))
    return None

a,b=breadth_first_search_graph(Jarritas)
print(f"Estas son las iteraciones {a} y este es el resultado {b}")