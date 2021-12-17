import sys

class Node:
    def __init__(self, state, parent=None):
        self.state = state
        self.parent = parent

        self.g = 0
        self.h = 0
    
    def __str__(self):
        return f'{self.state} g: {self.g} h: {self.h}'

    def __repr__(self):
        return self.__str__()

    def __eq__(self, other):
        if not isinstance(other, Node):
            return False

        for i in range(len(self.state)-1):
            for j in range(len(self.state[i])-1):
                if self.state[i][j] != other.state[i][j]:
                    return False
        
        return self.state[-1] == other.state[-1] and self.g == other.g and self.h == other.h
   
    def get_f(self): 
        return self.g + self.h
        

class Problema:

    def __init__(self, start, info_contenedor):
        self.start = start
        self.info_contenedor = info_contenedor
        self.open_lst = list()
        self.close_lst = list()

    def a_start_alg(self):
        # Initialize both open and closed list
        self.open_lst.append( self.start )

        # Loop until you find the end
        #while len(open_lst)>0:
        for i in range(20):
            print("***********************************************")
            print("iteracion: ", i)
            print("***********************************************")
            # Get the current node
            current = self.open_lst.pop(0)
            self.close_lst.append(current)

            if self.es_meta(current):
                print("llegué")
                return current

            children = self.getChildren(current)
            
            # Loop through children
            for child in children:
                # Check if this child is on the closed list
                if self.check_invalid_child(child):
                    continue
                
                if self.check_in_open_list(child):
                    continue
                
                self.open_lst = self.insertSorted(self.open_lst, child)

        return children

    def getChildren(self, estado:Node):
        children = list()

        # @Mapa_info es el estado del nodo
        mapa_info = estado.state
        puerto_actual = mapa_info[-1]["puerto"]
        
        # Si el barco esta en el puerto 0 y todos los contenedores estan en el barco   <- Hechas precondiciones [falta acciones]
        if puerto_actual == 0 and  \
                    self.contenedores_x_en_sitio_y(mapa_info[:-1], 1, 3) and \
                    self.contenedores_x_en_sitio_y(mapa_info[:-1], 2, 3):
            children.extend(self.navegar(estado, 1))

        # Si el barco esta en el puerto uno y ademas los contenedores que tienen que ir al puerto uno estan   <- Hechas precondiciones [falta acciones]
        # en el puerto uno y los contenedores que tienen que ir al puerto dos estan en el barco
        if puerto_actual == 1 and \
                    self.contenedores_x_en_sitio_y(mapa_info[:-1], 1, 1) and \
                    self.contenedores_x_en_sitio_y(mapa_info[:-1], 2, 3): 
            children.extend(self.navegar(estado, 2))

        for contenedor_i in range(len(estado.state) - 1):
                        
            posicion_contenedor = mapa_info[contenedor_i][0]

            # Comprobamos que la posi del barco sea la misma que el contenedor y que ademas que      <-  Hecho
            # el contenedor no tenga ninguna posicion del barco asignada
            if puerto_actual == posicion_contenedor and mapa_info[contenedor_i][1] is None:
                celdas = self.celdas_posibles(mapa_info, contenedor_i)
                if len(celdas) > 0:
                    children.extend(self.cargar_contenedor(estado, contenedor_i, celdas))

            # Barco en el puerto uno, con un contenedor que esta en el barco. Si se descargara                <-PENDIENTE [done i think]
            # uno que va al puerto 2 no pasa nada, porque antes de partir al puerto 2 hay que
            # volver a poner estos que se quedaron en el 1 --> metodo general para descargar contenedores en puerto uno
            if puerto_actual == 1 and posicion_contenedor == 3 and self.no_hay_nadie_encima(mapa_info, contenedor_i):
                children.extend(self.descargar(estado, contenedor_i, 1))

            # Barco en el puerto dos, con un contenedor en el barco, y ademas el puerto destino del           <-PENDIENTE [done i think]
            # contenedor es el puerto dos
            if puerto_actual == 2 and posicion_contenedor == 3 and self.no_hay_nadie_encima(mapa_info, contenedor_i):
                children.extend(self.descargar(estado, contenedor_i, 2))
        print("-------------------------------------------------------")
        for i in children:
            print(i)
        print("-------------------------------------------------------")
        return children

    # [------------- PRECONDICIONES ----------------]

    def celdas_posibles(self, estado:list, contenedor_i:int)->list:
        posibles = list()
        for celda in estado[-1].keys():
            
            if type(celda) != tuple: 
                continue

            posicion_debajo = ( celda[0], celda[1] + 1 )
            if posicion_debajo in estado[-1].keys():
                if not estado[-1][posicion_debajo][1]:
                    posibles.append(celda)
            else:
                posibles.append(celda)
                
        if self.info_contenedor[contenedor_i][0] == "R":
            nuevos_posibles = list()
            for i in posibles:
                if estado[-1][i][0] == "E":
                    nuevos_posibles.append(i)
            return nuevos_posibles
        else:
            return posibles
        
    def no_hay_nadie_encima(self, estado:list, contenedor_i:int):
        # Cogemos las coordenadas de misma pila, pero diferente depth (un depth menos es igual a una altura más)
        posicion_encima = ( estado[contenedor_i][1][0], estado[contenedor_i][1][1] - 1 ) #la pos del barco esta en la pos 1 del array del contenedor

        if posicion_encima in estado[-1].keys():    # posición legal dentro de la bahía
            return estado[-1][posicion_encima][1]      # esto retorna True si la posicion_encima está libre, False eoc
        else:
            return True # Caso en la que la posicion de arriba no esta contemplada en el barco
                        # por lo que no hay nada encima

    def contenedores_x_en_sitio_y(self, estado:list, destino:int, sitio_deseado:int):
        '''si un contenedor del puerto 'x' no esta en el sitio 'y' return False
            Ejemplos de combinaciones: 
                    x = 1 e y = 1 para "todos los contenedores tipo 1 en puerto 1
                    x = 2 e y = 3 para "todos los contenedores tipo 2 en barco" '''
        for contenedor in estado:
            
            # sacamos el id de la posicion del contenedor
            contenedor_i = estado.index(contenedor)
            # vemos cual es el destino del contenedor
            puerto_destino = self.info_contenedor[contenedor_i][1]
            # Sacamos donde se encuentra el contenedor
            sitio_actual = estado[contenedor_i][0]

            if puerto_destino == destino and sitio_actual != sitio_deseado: # tiene que estar en el barco para partir 
                return False

        return True

    # [------------- OPERADORES ----------------]

    def cargar_contenedor(self, estado:Node, contenedor_i:int, celdas:list):
        ''' Genera un nuevo estado por cada asignación entre "contenedor" y 
            cada celda libre '''
        nuevos = list()
        # iteramos sobre las celdas del barco hasta encontrar una libre
        info_barco = estado.state[-1]
        for celda in celdas:
            if type(celda) == tuple and info_barco[celda][1]:
                # copiamos el estado actual y lo modificamos cambiando el
                # contenedor de turno
                nuevo = self.mycopy(estado)
                nuevo.state[contenedor_i][0] = 3
                nuevo.state[contenedor_i][1] = celda
                nuevo.g = nuevo.g + 10 + celda[1]   #coste del operador
                # al terminar con esta celda libre, la marcamos como ocupada
                nuevo.state[-1][celda][1] = False
                nuevos.append(nuevo)

        return nuevos

    def descargar(self, estado:Node, contenedor_i:int, sitio:int):
        "metedo para descargar los contenedores que van a puerto x en el puerto y"
        # Coge posicion del estado actual
        posicion = estado.state[contenedor_i][1]
        nuevo = self.mycopy(estado)
        # Marcamos posicion como disponible de nuevo
        nuevo.state[-1][posicion][1] = True
        nuevo.state[contenedor_i][0] = sitio #marcamos sitio donde se ha descargado
        nuevo.state[contenedor_i][1] = None # No tiene coordenadas del barco
        nuevo.g = nuevo.g + 15 + 2*posicion[1]   #coste del operador
        return [ nuevo ]

    def navegar(self, estado:Node, destino:int):
        "Movemos el barco desde su posicon actual al destino indicado"
        nuevo = self.mycopy(estado)
        nuevo.state[-1]["puerto"] = destino
        nuevo.g = nuevo.g + 3500   #coste del operador
        return [ nuevo ]

    # [------------- OTROS ----------------]

    def insertSorted(self, lista:list, nodo:Node):
        print("///////////////////Listas ordenadas check///////////////////////")
        print("original")
        for i in lista:
            print(i)
            
        for i in range(len(lista)):
            if nodo.get_f() < lista[i].get_f():
                lista.insert(i, nodo)
                print("nodo entre medias")
                for i in lista:
                    print(i)
                print("///////////////////Listas ordenadas check///////////////////////")
                return lista

        lista.append(nodo)
        print("nodo al final")
        for i in lista:
            print(i)
        print("///////////////////Listas ordenadas check///////////////////////")
        return lista
        
    def check_invalid_child(self, node:Node):
        for closed_node in self.close_lst:
            if closed_node == node:
                return True
        return False

    def check_in_open_list(self, node):
        for open_node in self.open_lst:
            if node == open_node and node.get_f() >= open_node.get_f():
                return True
        return False

    def mycopy(self, estado:Node):
        # copiamos la lista de contenedores (todos menos el último)
        copia = list()
        for c in estado.state[:-1]:
            copia.append([])
            for e in c:
                copia[-1].append(e)

        # copiamos el diccionario del barco
        info_barco = dict()
        for k in estado.state[-1].keys():
            if type(k) == str:
                info_barco[k] = estado.state[-1][k]
            else:
                celda = list()
                for item in estado.state[-1][k]:
                    celda.append(item)
                info_barco[k] = celda
        
        copia.append(info_barco)

        nuevo = Node(copia, estado)
        nuevo.g = estado.g
        nuevo.h = estado.h

        return nuevo

    def es_meta(self, estado:Node):
        for c in estado.state[:-1]:
            destino = self.info_contenedor[estado.state.index(c)][1]
            if c[0] != destino:
                return False
        return True

        
if __name__ == "__main__":
    '''
    Contenedores
    1S1
    2S2
    3S2
    4R1
    Mapa
    N N
    N E
    '''
    S = Node([[0, None], [0, None], [0, None], [0, None],
              {"puerto": 0, (0,0): ["N", True], (0,1): ["N", True], (1,0): ["N", True], (1,1): ["E", True]}]
            )
    P = Problema( S, (("S", 1), ("S", 1), ("S", 2), ("R", 1)) )
    P.a_start_alg()

