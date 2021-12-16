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

        for i in range(len(self.state)-1):
            for j in range(len(self.state[i])-1):
                if self.state[i][j] != other.state[i][j]:
                    return False
        return True
    
    @property
    def g(self): return self._g
    @g.setter
    def g(self,value): self._g = value if type(value) == int else 1
    
    @property
    def h(self): return self._h
    @h.setter
    def h(self,value): self._h = value if type(value) == int else 1

    @property
    def f(self): return self._f
    @f.setter
    def f(self,value): self._f = value if type(value) == int else 1
        

class Problema:

    def __init__(self, start, info_contenedor):
        self.stat = start
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

                child.g += 1
                child.h = 0
                child.f = child.g + child.h

                if self.check_in_open_list(child):
                    continue
                
                open_lst.extend(children)

    def getChildern(self, estado:Node):
        children = list()

        for contenedor in estado.state[:-1]: 
            # @Mapa_info es el estado del nodo
            mapa_info = estado.state
            puerto_actual = mapa_info[-1]["puerto"]
            contenedor_i = mapa_info.index(contenedor)

            # Comprobamos que la posi del puerto sea la misma que el contenedor y que ademas que      <-  Hecho
            # el contenedor no tenga ninguna posicion del barco asignada
            if puerto_actual == contenedor[0] and contenedor[1] is None:
                children.extend(self.cargar_contenedor(estado, contenedor_i))

            # Barco en el puerto uno, con un contenedor que esta en el barco. Si se descargara                <-PENDIENTE
            # uno que va al puerto 2 no pasa nada, porque antes de partir al puerto 2 hay que
            # volver a poner estos que se quedaron en el 1
            if puerto_actual == 1 and contenedor[0] == 3 and self.no_hay_nadie_encima(mapa_info, contenedor_i):
                children.extend(self.descargar(estado, contenedor_i, 1))

            # Barco en el puerto dos, con un contenedor en el barco, y ademas el puerto destino del           <-PENDIENTE
            # contenedor es el puerto dos
            if puerto_actual == 2 and contenedor[0] == 3 and self.no_hay_nadie_encima(mapa_info, contenedor_i):
                children.extend(self.descargar(estado, contenedor_i, 2))

            # Si el barco esta en el puerto 0 y ademas todos los contenedores estan en el barco   <- Hechas precondiciones
            if puerto_actual == 0 and self.todos_los_contenedores_en(3, mapa_info[:-1]):
                children.extend(self.mover_p1(estado))

            # Si el barco esta en el puerto uno y ademas los contenedores que tienen que ir al puerto uno estan   <- Hechas precondiciones
            # en el puerto uno y los contenedores que tienen que ir al puerto dos estan en el barco
            if puerto_actual == 1 and self.contenedores_x_en_sitio_y(mapa_info, 1, 1) and self.contenedores_x_en_sitio_y(mapa_info, 2, 3): #self.todos_los_contenedores_1_en_1(mapa_info) and self.todos_los_contenedores_2_en_barco(mapa_info):
                children.extend(self.mover_p2())

        return children

    def mover_p1(self,estado):
        return
        
    def no_hay_nadie_encima(self, estado:list, contenedor_i:int):
        posicion_encima = ( estado[contenedor_i][0][0], estado[contenedor_i][0][1] - 1 )

        if posicion_encima in estado[-1].keys():    # posición legal dentro de la bahía
            return not estado[-1][posicion_encima]

    def contenedores_x_en_sitio_y(self, estado:list, destino:int, sitio_deseado:int):
        '''si un contenedor del puerto x no esta en el sitio y return False
        
            Combinaciones: x = 1 e y = 1 para "todos los contenedores tipo 1 en puerto 1
                           x = 2 e y = 3 para "todos los contenedores tipo 2 en barco" '''
        for contenedor in estado:

            contenedor_i = estado.index(contenedor)
            puerto_destino = self.info_contenedor[contenedor_i][1]
            sitio_actual = estado[contenedor_i][0]

            if puerto_destino == destino and sitio_actual != sitio_deseado:
                return False

        return True

    def cargar_contenedor(self, estado:Node, contenedor_i:int):
        ''' Genera un nuevo estado por cada asignación entre "contenedor" y 
            cada celda libre '''
        nuevos = list()
        # iteramos sobre las celdas del barco hasta encontrar una libre
        info_barco = estado[-1]
        for celda in info_barco.keys():
            if type(celda) == tuple and info_barco[celda][1]:
                # copiamos el estado actual y lo modificamos cambiando el
                # contenedor de turno
                nuevo = self.mycopy(estado)
                nuevo.state[contenedor_i][0] = 3
                nuevo.state[contenedor_i][1] = celda[0]
                # al terminar con esta celda libre, la marcamos como ocupada
                nuevo[-1][celda][1] = False
                nuevos.append(nuevo)
        return nuevos

    def descargar(self, estado:Node, contenedor_i:int, sitio:int):
        "metedo para descargar los contenedores que van a puerto x en el puerto x"
        posicion = estado.state[contenedor_i][1]
        nuevo = self.mycopy(estado)
        nuevo.state[-1][posicion][1] = True
        nuevo.state[contenedor_i][0] = sitio
        nuevo.state[contenedor_i][1] = None
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

    def todos_los_contenedores_en(self, sitio:int, estado:list):
        for contenedor in estado:
            if contenedor[0] != sitio:
                return False
        return True

    def calc_heurist(self, estado):
        return

        
if __name__ == "__main__":
    S = Node([[0, None], [0, None], [0, None], [0, None], {"puerto": 0, (0,0): ["N", True], (0,1): ["N", True], (1,0): ["N", True], (1,0): ["E", True]}])
    P = Problema( S, (("S", 1), ("S", 1), ("S", 2), ("R", 1)) )


'''# Si el barco esta en el puerto uno y ademas los contenedores estan en el barco
            # y ademas hay un contenedor que tiene que descargar en el puerto uno, entonces descarga  <-  Hecho
            if puerto == 1 \
                    and contenedor[0] == 3 \
                    and self.info_contenedor[contenedor_i][1] == 1:
                children.extend(self.descargar(estado, contenedor_i, 1))

            # Barco en el puerto uno, con un contenedor que esta en el barco y que ademas su puerto 
            # destino del contenedor es el puerto 2
            if puerto == 1 \
                    and contenedor[0] == 3 \
                    and self.info_contenedor[contenedor_i][1] == 2:
                children.extend(self.descargar(estado, contenedor_i, 1))'''