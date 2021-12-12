import sys
import constraint

class Celda:
    """ Clase que representa a una celda del barco. Toma su posición (fila
        y columna) y su tipo (normal, electrificada o prohibida) """
    def __init__(self, col, fila, tipo):
        # Fila en la que se sitia 
        self.fila = fila
        # Columna en la que se sitia
        self.col = col
        # Podemos apreciar que el par de coordenadas es (column, row)
        self.tipo = tipo
    
    def __gt__(self, other):
        # Metodo para ver cual celda es mayor que otra
        return self.fila + 1 == other.fila and self.col == other.col
    
    def __str__(self):
        # Metodo para poder imprimir el objeto por pantalla
        return "({}, {})".format(self.col, self.fila)
    
    def __repr__(self):
        return self.__str__()

class Contenedor:
    """ Clase que representa a un contenedor. Toma su identificador, 
        su tipo (normal o refrigerado) y su destino (puerto 1 o 2) """
    def __init__(self, id, tipo, destino):
        # Los id y el destino son numeros enteros para poder hacer comparaciones 
        # numericas en un futuro
        self.id = int(id)
        self.tipo = tipo
        self.destino = int(destino)

    def __lt__(self, other):
        # Metodo para ver si el contenedor es menor que otro 
        return self.id < other.id
    
    def __str__(self):
        # Metodo para poder imprimir el objeto por pantalla
        return str(self.id)
    
    def __repr__(self):
        return self.__str__()

class Problema:
    """ Clase que representa al problema. Contiene variables, dominios
        y restricciones. Recibe el esquema del barco y la lista de contenedores """
    def __init__(self, mapa, contenedores):
        
        # Creamos la tupla de variables como un vector de 'Contenedor'
        self.variables = list()
        for i in range(len(contenedores)):
            self.variables.append(Contenedor(contenedores[i][0], contenedores[i][1], contenedores[i][2]))
        self.variables = tuple(self.variables)

        # Creamos el dominio como un vector de 'Celda' examinando el mapa por columnas de arriba a abajo.
        # Cuando se lee una X, se asume que se llega a la base del barco y se procede con la siguiente
        # columna.

        self.dom = list()

        # Creamos la variable profundidades para ver la profundidad real del barco, es decir, hasta donde hay una 
        # X para que no se puedan posicionar ahi containers y por ende no queden flotando

        self.profundidades = list()
        for pila in range(len(mapa[0])):
            contador = 0
            for nivel in range(len(mapa)):
                if mapa[nivel][pila] == "X": break
                contador += 1
                self.dom.append( Celda(pila, nivel, mapa[nivel][pila]) )

            self.profundidades.append(contador - 1)

        # Creamos la variable problema para la futura resolucion
        self.problem = constraint.Problem()

        # add las variables con sus correspondientes dominios
        self.problem.addVariables(self.variables, self.dom)

        # seccion donde colocamos todas las constraints siedno la primera que todas las variables tomen 
        # valores del dominio difirentes, es decir, para que no haya dos contenedores en una celda por ejemplo
        self.problem.addConstraint(constraint.AllDifferentConstraint(), self.variables)
        self.problem.addConstraint(self.constraint_uno_debajo_de_otro, self.variables)
        self.problem.addConstraint(self.constraint_preferencias, self.variables)
        self.problem.addConstraint(self.constraint_refrigerados, self.variables)
        
    def solve(self):
        # Metodo para la resolucion final del problema
        return self.problem.getSolutions()

    def constraint_refrigerados(self, *args):
        # Metodo para ver que los containers Refrigerados se situen tan solo en celdas de energia 
        # En un momento ponemos como que la condicion planteada es True, es decir que esto se cumple
        condicion = True

        # Ahora iteramos sobre todos los argumentos pasados por la constraint
        for i in range(len(args)):
            # En caso de que la variable (container) sea refrigerador y esté colocado en una celda (dominio)
            # De tipo N, es decir, no energetica, la condicion pasa a ser False con ello, un tipo no valido
            if self.variables[i].tipo == "R" and args[i].tipo == "N":
                condicion = False
        
        return condicion

    def constraint_uno_debajo_de_otro(self, *args):
        # i = uno, j = otro
        # Metodo para checkear que hay un container debajo de otro y que con ello no haya containers volando felices
        for i in range(len(args)):
            # vecto de condiciones para ver si se llegan a cumplir todas ellas
            condicion = []
            for j in range(len(args)):
                # Condicion de que si i y j son diferentes (son dos containers diferentes), que ademas la diferencia de niveles sea uno como mucho, con 
                # esto conseguimos que no vueles, ya que estaran uno encima de otros, tambien importante que esten los dos containers en la misma
                # columna porque si no, no tiene sentido hacer esta comprobacion, y qie por ultimo que se este ocupando primeramente el hueco 
                # mas profundo que haya
                if( i != j and args[j].fila - args[i].fila == 1 and args[i].col == args[j].col or args[i].fila == self.profundidades[args[i].col]):
                    # Si todo esto se cumple se hace un add de true a la lista de las condiciones
                    condicion.append(True)
            # si para un i no se ha encontrado ningún j que satisfaga el condicional, termina
            '''res = False
            for i in condicion:
                if i == True:
                    res = True
            if res == False:
                return False'''

            if len(condicion) == 0:
                return False

        return True

    def constraint_preferencias(self, *args):
        # Que los del puerto dos esten debajo
        # i = primero // j = otro
                   
        for i in range(len(args)):
            # Partimos creyendo que esta condicion se cumple hasta que se demuestre lo contrario
            condicion = True
            for j in range(len(args)):                
                #si puerto == 2 y debajo puerto == 1: False        
                if (i != j and self.variables[i].destino == 2 and \
                        ( args[i].col == args[j].col and args[j].fila > args[i].fila and \
                                (self.variables[j].destino == 1)
                        )
                    ):
                    condicion = False
            if not condicion:
                return False
        return True


def read_doc(path, file):
    # metodo para leer los documentos pasados por el usuario
    res = []
    with open(path + "/" + file) as infile:
        lectura = infile.readline().split(" ")
        lectura[-1] = lectura[-1].replace("\n", "")
        while len(lectura) > 0 and lectura[0] != '':
            res.append(lectura)
            lectura = infile.readline().split(" ")
            lectura[-1] = lectura[-1].replace("\n", "")
    return res

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Debe introducir: CSPStowage.py <path> <mapa> <contenedores>")
        quit()
    mapa = read_doc(sys.argv[1], sys.argv[2])        
    contenedores = read_doc(sys.argv[1], sys.argv[3])
    # variable res para el futuro resultado retornado
    res = ""
    try:
        res = Problema(mapa, contenedores).solve()
    except:
        pass
    
    # escribimos el resultado en el documento de salida especificado
    with open(f'{sys.argv[1]}/{sys.argv[2]}-{sys.argv[3]}.output', 'w', encoding="UTF-8") as outfile:
        outfile.write("Número de soluciones: {}\n".format(len(res)))
        for d in res:
            outfile.write(str(d) + "\n")
