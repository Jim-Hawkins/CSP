import sys
import constraint

class Punto:
    def __init__(self, col, fila, tipo):
        self.fila = fila
        self.col = col
        self.tipo = tipo
    
    def __gt__(self, other):
        #if self.fila == other.fila:
        #    return self.col > self.col
        return self.fila + 1 == other.fila and self.col == other.col
    
    def __str__(self):
        return "({}, {})".format(self.col, self.fila)
    
    def __repr__(self):
        return self.__str__()

class Contenedor:
    def __init__(self, id, tipo, destino):
        self.id = int(id)
        self.tipo = tipo
        self.destino = int(destino)

    def __lt__(self, other):
        return self.id < other.id
    
    def __str__(self):
        #return f'{self.id}{self.tipo}{self.destino}'
        return str(self.id)
    
    def __repr__(self):
        return self.__str__()

class Problema:
    def __init__(self, mapa, contenedores):

        # Comprobamos que haya suficientes celdas E para los contenedores R
        if self.contar_celdas(mapa, "E") < self.contar_contenedores(contenedores, "R"):
            print( "No hay suficientes celdas electrificadas")
            raise

        self.variables = list()
        for i in range(len(contenedores)):
            self.variables.append(Contenedor(contenedores[i][0], contenedores[i][1], contenedores[i][2]))
        self.variables = tuple(self.variables)

        self.dom = list()
        self.profundidades = list()
        for pila in range(len(mapa[0])):
            contador = 0
            for nivel in range(len(mapa)):
                if mapa[nivel][pila] == "X": break
                contador += 1
                self.dom.append( Punto(pila, nivel, mapa[nivel][pila]) )

            self.profundidades.append(contador - 1)

        #print(self.profundidades)
        self.problem = constraint.Problem()
        self.problem.addVariables(self.variables, self.dom)

        self.problem.addConstraint(constraint.AllDifferentConstraint(), self.variables)
        self.problem.addConstraint(self.constraint_uno_debajo_de_otro, self.variables)
        self.problem.addConstraint(self.constraint_preferencias, self.variables)
        self.problem.addConstraint(self.constraint_refrigerados, self.variables)
        
    def solve(self):
        return self.problem.getSolutions()

    def constraint_refrigerados(self, *args):
        condicion = True
        for i in range(len(args)):
            if self.variables[i].tipo == "R" and args[i].tipo == "N":
                condicion = False
        
        return condicion

    def constraint_uno_debajo_de_otro(self, *args):
        # i = uno, j = otro
        for i in range(len(args)):
            condicion = []
            for j in range(len(args)):
                if( i != j and args[j].fila - args[i].fila == 1 and args[i].col == args[j].col or args[i].fila == self.profundidades[args[i].col]):
                    condicion.append(True)
            # si para un i no se ha encontrado ningún j que satisfaga el condicional, termina
            res = False
            for i in condicion:
                if i == True:
                    res = True
            if res == False:
                return False
            '''if len(condicion) == 0:
                return False'''

        return True

    def constraint_preferencias(self, *args):
        # Que los del puerto dos esten debajo
        # i = primero // j = otro
        #print(self.variables)
                   
        for i in range(len(args)):
            condicion = True
            for j in range(len(args)):
                
                '''if( i != j and args[i].col == args[j].col and self.variables[i].destino >= self.variables[j].destino):
                    condicion = True
            
            if not condicion:
                return False
        
        return True'''
                #si puerto == 1 y (debajo puerto == 1 o puerto == 2 o está en la base): True
                '''if (self.variables[i].destino == 1 and \
                        ( args[i].col == args[j].col and args[j].fila - args[i].fila == 1 and \
                                (self.variables[j].destino == 1 or self.variables[j].destino == 2 or args[i].fila == 2)
                        )
                    ):
                    condicion = True
                #si puerto == 2 y (debajo puerto == 2 o está en la base): True
                if (self.variables[i].destino == 2 and \
                        ( args[i].col == args[j].col and args[j].fila - args[i].fila == 1 and \
                                (self.variables[j].destino == 2 or args[i].fila == 2)
                        )
                    ):
                    condicion = True'''
                
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

    def encuentra_celdas(self, contenedores, tipo):
        res = list()
        for i in range(len(contenedores)):
            for j in range(len(contenedores[0])):
                if contenedores[i][j] == tipo:
                    res.append( (i,j) )
        return res

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

    def contar_contenedores(self, lista, tipo):
        contador = 0
        for cont in lista:
            if tipo in cont:
                contador += 1
        return contador

    def contar_celdas(self, lista_de_listas, tipo=""):
        contador = 0
        for fila in lista_de_listas:
            for c in fila:
                if tipo in c:
                    contador += 1
        return contador



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
    res = ""
    try:
        res = Problema(mapa, contenedores).solve()
    except:
        pass

    for i in res:
        print(i)

    with open(f'{sys.argv[2]}-{sys.argv[3]}.output', 'w') as outfile:
        outfile.write("Número de soluciones: {}\n".format(len(res)))
        for d in res:
            outfile.write(str(d) + "\n")
