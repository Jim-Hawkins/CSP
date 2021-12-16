import sys

class Node:
    def __init__(self, state, parent=None):
        self.state = state
        self.parent = parent

        self._g = 0
        self._h = 0
        self._f = 0
    
    def __str__(self):
        return f'{self.state}'

    def __eq__(self, other):
        if not isinstance(other, Node):
            return False

        for i in range(len(self.state)):
            for j in range(len(self.state[i])):
                if self.state[i][j] != other.state[i][j]:
                    return False
        return True
    
    @property
    def g(self):
        return self._g
    
    @g.setter
    def g(self,value):
        self._g = value
    
    @property
    def h(self):
        return self._h
    
    @h.setter
    def h(self,value):
        self._h = value

    @property
    def f(self):
        return self._f
    
    @f.setter
    def f(self,value):
        self._f = value
        


class Problema:

    def __init__(self, start, info_contenedor, info_barco):
        self.stat = start
        self.info_barco = info_barco
        self.info_contenedor = info_contenedor

    def a_start_alg(self):
        # Initialize both open and closed list
        open_lst = list(self.start)
        close_lst = list()

        # Loop until you find the end
        while len(open_lst)>0:

            # Get the current node
            current = open_lst.pop(0)
            close_lst.append(current)

            if self.es_meta(current):
                print("llegué")
                return current

            children = self.getChildren(current)
            
            # Loop through children
            for child in children:
                # Check if this child is on the closed list
                if self.check_invalid_child(child):
                    continue

                child.g = current.g + 1
                child.h = 0
                child.f = child.g + child.h

                if self.check_in_open_list(child):
                    continue
                
                open_lst.extend(children)

    def getChildern(self, estado):
        children = list()

        for contenedor in estado.state[:-1]: 
            if estado[-1] == contenedor[1] \
                    and contenedor[1] is None:
                children.extend(self.cargar_contenedor(estado, estado.state.index(contenedor)))

            if estado[-1] == 1 \
                    and contenedor[0] == 3 \
                    and self.info_contenedor[estado.state.index(contenedor)][1] == 1:
                children.extend(self.descargar_c1_p1(estado, estado.state.index(contenedor)))

            if estado[-1] == 1 \
                    and contenedor[0] == 3 \
                    and self.info_contenedor[estado.state.index(contenedor)][1] == 2:
                children.extend(self.descargar_c2_p1(estado, estado.state.index(contenedor)))

            if estado[-1] == 2 \
                    and contenedor[0] == 3 \
                    and self.info_contenedor[estado.state.index(contenedor)][1] == 2:
                children.extend(self.descargar_c2_p2(estado, estado.state.index(contenedor)))

            if estado[-1] == 0 \
                    and self.todos_los_contenedores_en(3, estado):
                children.extend(self.mover_p1(estado))

            if estado[-1] == 1 and self.todos_los_contenedores_en(1, estado.state) and self.todos_los_contenedores_en(3, estado.state):
                children.extend(self.mover_p2())


        return children

    def mover_p1(self,estado):
        pass
        

    def cargar_contenedor(self, estado:Node, contenedor:int):
        ''' Genera un nuevo estado por cada asignación entre "contenedor" y 
            cada celda libre '''
        nuevos = list()
        # iteramos sobre las celdas del barco hasta encontrar una libre
        for celda in self.info_barco.keys():
            if self.info_barco[celda][1]:
                # copiamos el estado actual y lo modificamos cambiando el
                # contenedor de turno
                nuevo = self.mycopy(estado)
                nuevo.state[contenedor][0] = 3
                nuevo.state[contenedor][1] = celda[0]
                nuevos.append(nuevo)
                # cuando terminamos con esta celda libre, la marcamos como ocupada
                self.info_barco[celda][1] = False
        return nuevos

    def descargar_c1_p1(self, estado:Node, contenedor:int):
        posicion = estado[contenedor][1]
        self.info_barco[posicion][1] = True

        nuevo = self.mycopy(estado)
        nuevo.state[contenedor][0] = 1
        nuevo.state[contenedor][1] = None
        return nuevo

    def check_invalid_child(self, node):
        for closed_node in self.close_lst:
            if closed_node == child:
                return True
        return False

    def check_in_open_list(self, node):
        return

    def mycopy(self, estado:Node):
        copia = list()
        for c in estado.state:
            copia.append([])
            for e in c:
                copia[-1].append(e)
        return Node(copia, estado)

    def es_meta(self, estado):
        for c in estado:
            if type(c) == list:
                return
        return True

    def todos_los_contenedores_en(self, sitio, estado):
        for contenedor in estado:
            if contenedor[0] != sitio:
                return False
        return True

    def calc_heurist(self, estado):
        return

        
if __name__ == "__main__":
    S = Node([[0, None], [0, None], [0, None], [0, None], 0])
    P = Problema( S, 
                 (("S", 1), ("S", 1), ("S", 2), ("R", 1)), 
                 {(0,0): ["N", True], (0,1): ["N", True], (1,0): ["N", True], (1,0): ["E", True]})
