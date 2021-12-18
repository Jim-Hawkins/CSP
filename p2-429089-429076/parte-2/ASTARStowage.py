import sys
import time

class Node:
    def __init__(self, state, parent=None):
        # Parametros de la clase nodo-> padre, y el estado interno
        self.state = state
        self.parent = parent

        # Valores para sacar la funcion f()
        self.g = 0
        self.h = 0

        # Para retornar en un futuro los procesos que se han llevado a termino
        self.action = ""
    
    def get_f(self): 
        # Retorna el valor de f(), la suma de g y h 
        return self.g + self.h

    def __str__(self):
        return f'{self.state} g: {self.g} h: {self.h}'

    def __repr__(self):
        return self.__str__()

    def __eq__(self, other):
        # Comprobamos que hace el igual con otro nodo
        if not isinstance(other, Node):
            return False

        # Comparemos cada uno de los elementos del estado del nodo
        for i in range(len(self.state)-1):
            for j in range(len(self.state[i])-1):
                if self.state[i][j] != other.state[i][j]:
                    return False
        
        return self.state[-1] == other.state[-1]

    def __le__(self, other):
        return self.get_f() <= other.get_f()

    def __gt__(self, other):
        return self.get_f() > other.get_f()
   

class Problema:

    # Al problema se le tiene que pasar el nodo inicial, la info de los contenedores (estatica)
    # y la heuristica a usar
    def __init__(self, start, info_contenedor, heuristica):
        self.start = start
        self.info_contenedor = info_contenedor
        self.heuristica = heuristica
        self.max_iteraciones = 9000
        # Creamos las dos listas, abiertos y cerrados
        self.abierta = list()
        self.cerrada = list()

    def a_start_alg(self):
        # Iniciamos cronometro
        t_inicio = time.time()

        self.abierta.append( self.start )
        # Contador para los pasos que da el proceso
        i = -1
        # El algoritmo busca mientras le queden nodos por expandir
        while len(self.abierta) and i < self.max_iteraciones:
            i += 1
            # Tomamos el estado actual y lo añadimos a cerrada
            current = self.abierta.pop(0)
            self.cerrada.append(current)
            
            # En caso de que el nodo sea nodo meta, recogemos las estadisticas y terminamos
            if self.es_meta(current):
                stats = [
                            time.time() - t_inicio,
                            current.get_f(),
                            None,
                            len(self.cerrada)
                        ]
                print("Solución encontrada")
                return self.back_path(current), stats

            # Generamos los sucesores del nodo actual
            children = self.getChildren(current)

            '''print("-----------------------------------")
            print("iteracion: ",i)
            for a in children:
                print(a)
            print("-----------------------------------")'''

            for child in children:
                # Filtramos los hijos que ya estén en abierta o cerrada
                if self.check_cerrado(child) or self.check_abierto(child):
                    continue
                
                # Organizamos la lista de menor a mayor coste
                self.abierta = self.insertSorted(self.abierta, child)
                
        
        # Si no hubiera solución, hay que devolver algo
        print("No se ha encontrado ninguna solución")
        stats = [ time.time() - t_inicio, float('inf'), None, float('inf') ]
        if i < self.max_iteraciones:
            texto = "No existe solución\n"
        else:
            texto = "No se encontró solución en {} iteraciones\n".format(i)
        return texto, stats

    def getChildren(self, estado:Node):
        children = list()

        # @Mapa_info es el estado del nodo
        mapa_info = estado.state
        puerto_actual = mapa_info[-1]["puerto"]
        
        # El barco puede avanzar siempre que no esté en el puerto 2, que es el final
        if puerto_actual < 2:
            children.append(self.navegar(estado))

        for contenedor_i in range(len(estado.state) - 1):
            posicion_contenedor = mapa_info[contenedor_i][0]

            # Comprobamos que el barco y el contenedor están en el mismo sitio y que
            # el contenedor no esté en el barco
            if puerto_actual == posicion_contenedor and mapa_info[contenedor_i][1] is None:
                celdas = self.celdas_posibles(mapa_info, contenedor_i)
                for celda in celdas:
                    children.append(self.cargar(estado, contenedor_i, celda))
                
            # Comprobamos que el contenedor está en el barco y no tiene a ninguno encima
            if posicion_contenedor == 3 and self.no_hay_nadie_encima(mapa_info, contenedor_i):
                children.append(self.descargar(estado, contenedor_i, puerto_actual))
        
        return children

    # [------------- PRECONDICIONES ----------------]

    def celdas_posibles(self, estado:list, contenedor_i:int)->list:
        ''' Método para decidir qué celdas puede ocupar un contenedor eliminando
            casos imposibles (restricciones gravedad y tipo de contenedor) '''
        info_barco = estado[-1]
        posibles = list()
        for celda in info_barco.keys():
            # No todas las claves son celdas; Descartamos las celdas ocupadas (en False)
            if type(celda) != tuple or not info_barco[celda][1]: continue
            # Generamos la celda que estaría debajo
            posicion_debajo = ( celda[0], celda[1] + 1 )
            # ¿Esa celda existe de verdad?
            if posicion_debajo in info_barco.keys():
                # Solo cogemos la celda si la de debajo está ocupada (gravedad)
                if not info_barco[posicion_debajo][1]:
                    posibles.append(celda)
            else:
                # Si no existe nada debajo de la celda, es que está en la base, correcto
                posibles.append(celda)
        
        # Una vez satisfecha la gravedad, si el contenedor es R, reducimos sus
        # posibilidades a celdas E
        if self.info_contenedor[contenedor_i][0] == "R":
            nuevos_posibles = list()
            for i in posibles:
                if info_barco[i][0] == "E":
                    nuevos_posibles.append(i)
            return nuevos_posibles
        else:
            return posibles
        
    def no_hay_nadie_encima(self, estado:list, contenedor_i:int):
        ''' Método que decide si encima no hay contenedores, para poder descargarlo '''
        # Generamos la celda que estaría encima
        posicion_encima = ( estado[contenedor_i][1][0], estado[contenedor_i][1][1] - 1 ) #la pos del barco esta en la pos 1 del array del contenedor
        # ¿Esa celda existe de verdad?
        if posicion_encima in estado[-1].keys():
            # Devuelve el estado de la celda de arriba (True si está libre, False eoc)
            return estado[-1][posicion_encima][1]
        else:
            # Si no existe nada encima, es que está en la superficie, correcto
            return True

    # [------------- OPERADORES ----------------]

    def cargar(self, estado:Node, contenedor_i:int, celda:tuple):
        ''' Carga un contenedor en una celda del barco '''

        nuevo = self.mycopy(estado)                 # Generamos el hijo y para modificarlo
        nuevo.state[contenedor_i][0] = 3            # Contenedor en el barco
        nuevo.state[contenedor_i][1] = celda        # Posición dentro del barco
        nuevo.state[-1][celda][1] = False           # Marcar celda como ocupada
        nuevo.action = f'cargar (contenedor: {contenedor_i + 1}, en: {celda})'
        nuevo.g = nuevo.g + 10 + celda[1]           # Coste del operador
        if self.heuristica == 1:                    # Cálculo de la heuristica
            nuevo.h = self.heur_1(nuevo)
        else:
            nuevo.h = self.heur_2(nuevo)

        return nuevo

    def descargar(self, estado:Node, contenedor_i:int, sitio:int):
        ''' Descarga un contenedor en un puerto '''

        posicion = estado.state[contenedor_i][1]    # Celda actual del contenedor
        nuevo = self.mycopy(estado)                 # Generamos el hijo y para modificarlo
        nuevo.state[contenedor_i][0] = sitio        # Contenedor el el sitio donde se descargue
        nuevo.state[-1][posicion][1] = True         # Marcar celda como libre
        nuevo.state[contenedor_i][1] = None         # Ya no está en el barco
        nuevo.action = f'descargar (contenedor: {contenedor_i + 1}, en puerto: {sitio})'
        nuevo.g = nuevo.g + 15 + 2*posicion[1]      # Coste del operador
        if self.heuristica == 1:                    # Cálculo de la heuristica
            nuevo.h = self.heur_1(nuevo)
        else:
            nuevo.h = self.heur_2(nuevo)
        
        return nuevo

    def navegar(self, estado:Node):
        ''' El barco se desplaza al siguiente puerto '''
        puerto_actual = estado.state[-1]["puerto"]
        nuevo = self.mycopy(estado)                   # Generamos el hijo y para modificarlo
        nuevo.state[-1]["puerto"] = puerto_actual + 1 # El barco se va al siguiente puerto
        nuevo.action = f'navegar (a puerto: {puerto_actual + 1})'
        nuevo.g = nuevo.g + 3500                      # Coste del operador
        if self.heuristica == 1:                      # Cálculo de la heuristica
            nuevo.h = self.heur_1(nuevo)
        else:
            nuevo.h = self.heur_2(nuevo)

        return nuevo

    # [-------- HEURÍSTICAS ---------------]
    
    def heur_1(self, estado:Node):
        ''' Heurística que cuenta cuántos nodos faltan por llevar a su destino '''
        total_mal = len(estado.state)-1
        
        for contenedor_i in range(len(estado.state) -1):
            # Por cada contenedor en su sitio se va reduciendo el coste
            if estado.state[contenedor_i][0] == self.info_contenedor[contenedor_i][1]:
                total_mal -= 1
                                
        return total_mal 
        
    def heur_2(self, estado:Node):
        ''' Heuristica que cuenta los contenedores que el barco deja atrás '''
        
        # si los contenedores estan con el barco o en su puerto, se premia 
        total_coste = 0
        for contenedor_i in range(len(estado.state) -1):
            # vemos que el contenedor no este en el mismo puerto que el barco
            if estado.state[contenedor_i][0] != estado.state[-1]["puerto"]: 
                # Vemos que si ese no es su destino
                if estado.state[contenedor_i][0] != self.info_contenedor[contenedor_i][1]:
                    # Se le olvido cargarlo al barco
                    total_coste += 50 #sumamos cicuenta al coste
        
        return total_coste

    # [------------- OTROS ----------------]

    def back_path(self, estado:Node):
        "metodo para obtener todo el camino del problema"
        pasos = list()
        path = ""
        current = estado
        while current is not None:
            pasos.append(current.action)
            current = current.parent

        pasos = pasos[::-1]
        pasos = pasos[1:]
        for i, act in enumerate(pasos):
            path += f'{i+1}. {pasos[i]}\n'
        return path

    def insertSorted(self, lista:list, nodo:Node):
        """ Método para insertar ordenadamente en la lista abierta """
        for i in range(len(lista)):
            if nodo.get_f() < lista[i].get_f():
                lista.insert(i, nodo)
                return lista

        lista.append(nodo)
        return lista
        
    def check_cerrado(self, node:Node):
        # Nodo invalido si está en la lista de cerrados (ya expandido con menor coste)
        for closed_node in self.cerrada:
            if closed_node == node:
                return True
        return False

    def check_abierto(self, node):
        # Nodo invalido si está en la lista de abiertos y tiene un coste igual 
        # o superior a su duplicado
        delete = False
        for i, open_node in enumerate(self.abierta):
            if node == open_node:
                # Si tiene un clon en abierta y su coste es peor, lo desechamos
                if node.get_f() >= open_node.get_f():
                    return True
                # Si el coste del nodo es mejor que el del clon, dejamos de iterar
                # y eliminamos el que tiene mayor coste
                else:
                    delete = True
                    break
        if delete:
            self.abierta.remove(self.abierta[i])

        return False

    def mycopy(self, estado:Node):
        # copiamos la lista de contenedores (todos los elementos menos el 
        # último del estado)
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
        ''' El estado es meta si todos los contenedores están en su destino '''
        for c in range(len(estado.state) - 1):
            destino = self.info_contenedor[c][1]
            if estado.state[c][0] != destino:
                return False
        return True

        

def store_data(info, nombre_archivo):
    "Metodo para guardar la info final del problema"

    with open(f'ASTAR-tests/{nombre_archivo}.output', "w", encoding="utf-8") as outfile:
        outfile.write(info[0])

    with open(f'ASTAR-tests/{nombre_archivo}.stat', "w", encoding="utf-8") as outfile:
        outfile.write("Tiempo total: " + str(info[1][0]) + "\n")
        outfile.write("Coste total: " + str(info[1][1]) + "\n")
        outfile.write("Longitud del plan: " + str(len(info[0].split("\n"))) + "\n")
        outfile.write("Nodos expandidos: " + str(info[1][3]) + "\n")

def read_doc(mapa_path, contenedores):
    "Metodo para leer los datos pasados por los archivos"
    estado = list()
    cont_info = list()
    mapa = list()
    
    with open("ASTAR-tests/" + contenedores, "r") as cont_file:
        lectura = cont_file.readline().split(" ")
        lectura[-1] = lectura[-1].replace("\n", "")
        while len(lectura) > 0 and lectura[0] != '':
            # representante del contenedor i-ésimo
            estado.append([0, None])
            # tipo y destino del contenedor i-ésimo
            cont_info.append( (lectura[1], int(lectura[2])) )

            lectura = cont_file.readline().split(" ")
            lectura[-1] = lectura[-1].replace("\n", "")
    
    estado.append( {"puerto": 0} )
    cont_info = tuple(cont_info)

    with open("ASTAR-tests/" + mapa_path, "r") as map_file:
        lectura = map_file.readline().split(" ")
        lectura[-1] = lectura[-1].replace("\n", "")
        while len(lectura) > 0 and lectura[0] != '':
            
            mapa.append(lectura)

            lectura = map_file.readline().split(" ")
            lectura[-1] = lectura[-1].replace("\n", "")

    for fila in range(len(mapa)):
        for columna in range(len(mapa[fila])):
            if mapa[fila][columna] != "X":
                estado[-1][ (columna, fila) ] = [mapa[fila][columna], True]

    return estado, cont_info
        
if __name__ == "__main__":

    estado_inicial, contenedores = read_doc(sys.argv[1], sys.argv[2])
    S = Node(estado_inicial)
    P = Problema( S, contenedores, int(sys.argv[3]))
    info = P.a_start_alg()
    store_data(info, f'{sys.argv[1]}-{sys.argv[2]}-{sys.argv[3]}')
    
    

