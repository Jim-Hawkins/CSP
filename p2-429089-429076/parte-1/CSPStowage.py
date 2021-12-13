import sys
import constraint

class Celda:
    """ Clase que representa a una celda del barco. Toma su posición (fila
        y columna) y su tipo (normal, N; electrificada, E; o prohibida, X) """
    def __init__(self, col, fila, tipo):
        self.fila = fila
        self.col = col
        self.tipo = tipo
    
    def __gt__(self, other):
        # Metodo que implementa el operador ">" para Celda
        return self.fila + 1 == other.fila and self.col == other.col
    
    def __str__(self):
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
        # Metodo que implementa el operador "<" para Contenedor
        return self.id < other.id
    
    def __str__(self):
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

        # 'dominio' es un vector de 'Celda' 
        self.dom = list()

        # Creamos la variable 'profundidades' para ver la profundidad real del 
        # barco, es decir, hasta donde hay una X, que representa la base
        self.profundidades = list()
        
        # Creamos el dominio examinando el mapa por columnas de arriba a abajo. 
        for pila in range(len(mapa[0])):
            nivel = 0
            while nivel < len(mapa) and mapa[nivel][pila] != "X":
                self.dom.append( Celda(pila, nivel, mapa[nivel][pila]) )
                nivel += 1
            self.profundidades.append(nivel-1)

        # Creamos la variable problema para la futura resolucion
        self.problem = constraint.Problem()

        # add las variables con sus correspondientes dominios
        self.problem.addVariables(self.variables, self.dom)

        # Restricciones del problema
        self.problem.addConstraint(constraint.AllDifferentConstraint(), self.variables)
        self.problem.addConstraint(self.constraint_uno_debajo_de_otro, self.variables)
        self.problem.addConstraint(self.constraint_preferencias, self.variables)
        self.problem.addConstraint(self.constraint_refrigerados, self.variables)
        
    def solve(self):
        ''' Metodo para la resolucion final del problema '''
        return self.problem.getSolutions()

    def constraint_refrigerados(self, *args):
        ''' Restricción que hace que que los containers Refrigerados se sitúen tan 
            solo en celdas E '''
        condicion = True
        for i in range(len(args)):
            # Si el contenedor i-ésimo es refrigerado y está colocado en una celda
            # de tipo N, la condicion pasa a ser False para descartar esta opción
            if self.variables[i].tipo == "R" and args[i].tipo == "N":
                condicion = False
        
        return condicion

    def constraint_uno_debajo_de_otro(self, *args):
        ''' Restricción que comprueba si un container está en la base o tiene a
            otro encima y que con ello no haya containers volando felices '''
        # i = uno, j = otro
        for i in range(len(args)):
            # vector de booleanos para detectar si algún valor cumple la restricción
            condicion = []
            # si el elemento i-ésimo está en la base, cumple la restricción
            if args[i].fila == self.profundidades[args[i].col]: 
                condicion.append(True)
            for j in range(len(args)):
                # Condición que se cumple si la diferencia de niveles es una unidad
                # (con esto conseguimos que no vuelen, ya que estarán uno encima de
                # otro) y si están ambos en la misma pila
                if (i != j and args[j].fila - args[i].fila == 1 and args[i].col == args[j].col):
                    condicion.append(True)
            # si para un i no se ha encontrado ningún j que satisfaga el condicional, termina
            if len(condicion) == 0:
                return False

        return True

    def constraint_preferencias(self, *args):
        ''' Restricción que comprueba que los contenedores que van al puerto 
            2 estén en la base o debajo tengan a otro que vaya al puerto 2 '''                   
        for i in range(len(args)):
            # Partimos creyendo que esta condicion se cumple hasta que se demuestre lo contrario
            condicion = True
            for j in range(len(args)):                
                #si puerto == 2 y debajo puerto == 1: se incumple la restricción        
                if (i != j and self.variables[i].destino == 2 and
                        ( args[i].col == args[j].col and args[j].fila > args[i].fila and
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
    # variable para almacenar resultado del problema
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
