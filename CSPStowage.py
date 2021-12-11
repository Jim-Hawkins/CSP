import sys
import constraint

class Punto:
    def __init__(self, col, fila):
        self.fila = fila
        self.col = col
    
    def __gt__(self, other):
        #if self.fila == other.fila:
        #    return self.col > self.col
        #print(self, other, self.fila == other.fila + 1 and self.col == other.col)
        return self.fila + 1 == other.fila and self.col == other.col
    
    def __str__(self):
        return "({}, {})".format(self.col, self.fila)
    
    def __repr__(self):
        return self.__str__()

class Problema:
    def __init__(self, mapa, contenedores):

        self.variables = list()
        for i in range(len(contenedores)):
            self.variables.append(f'{contenedores[i][0]}{contenedores[i][1]}{contenedores[i][2]}')

        self.variables = tuple(self.variables)

        self.dom = list()
        for pila in range(len(mapa[0])):
            for nivel in range(len(mapa)):
                self.dom.append( Punto(pila, nivel) )

        self.problem = constraint.Problem()
        self.problem.addVariables(self.variables, self.dom)

        #prohibidos = encuentra_celdas(contenedores, "X")
        #electrificados = encuentra_celdas(contenedores, "E")

        self.problem.addConstraint(constraint.AllDifferentConstraint(), self.variables)
        
        self.problem.addConstraint(self.constraint_uno_debajo_de_otro, self.variables)
        
        
        '''problem.addConstraint(constraint_prohibidos, 
                            (variables, prohibidos))
        problem.addConstraint(constraint_contenedores_ordenados, 
                            variables)
        problem.addConstraint(constraint_suficientes_celdas, 
                            (mapa, contenedores, "E", "R"))
        problem.addConstraint(constraint_suficientes_celdas, 
                            (mapa, contenedores, "N", "S"))'''
        
    def solve(self):
        return self.problem.getSolutions()

    def constraint_base(self, *args):
        for i in range(len(args)):
            pass

    def constraint_uno_debajo_de_otro(self, *args):
        # i = uno, j = otro
        for i in range(len(args)):
            condicion = []
            for j in range(len(args)):
                if( i != j and args[j].fila - args[i].fila == 1 and args[i].col == args[j].col or args[i].fila == 2):
                    condicion.append(True)
            # si para un i no se ha encontrado ningún j que satisfaga el condicional, termina
            res = False
            for i in condicion:
                if i == True:
                    res = True
            if res == False:
                return False

        return True

    def constraint_uno_encima_de_otro(self, *args):
        # i = uno, j = otro
        for i in range(len(args)):
            for j in range(i+1, len(args)):
                if args[j].fila == 2:
                    if not ( (args[i].fila - args[j].fila == -1 and args[i].col == args[j].col) ):
                        return False
        return True
    
    def encuentra_celdas(self, contenedores, tipo):
        res = list()
        for i in range(len(contenedores)):
            for j in range(len(contenedores[0])):
                if contenedores[i][j] == tipo:
                    res.append( (i,j) )
        return res

    def constraint_prohibidos(self, cont, prohibidos):
        return cont not in prohibidos

    def constraint_suficientes_celdas(self, mapa, contenedores, tipo_celda, tipo_cont):
        ''' Función que determina que si hay suficientes celdas de un tipo para
            acomodar a determinado tipo de cont'''
        celda = 0
        for i in range(len(mapa)):
            for j in range(len(mapa[0])):
                if mapa[i][j] == tipo_celda:
                    celda += 1
        cont = 0
        for i in range(len(contenedores)):
            if i[1] == tipo_cont:
                cont += 1
        
        return celda >= cont


def read_doc(path, file):
    res = []
    with open(path + "/" + file) as infile:
        lectura = infile.readline().split(" ")
        lectura[-1] = lectura[-1].replace("\n", "")
        while len(lectura) != 1:
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
    res = Problema(mapa, contenedores).solve()

    for i in res:
        print(i)
