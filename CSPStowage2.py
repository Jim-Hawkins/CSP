import sys
import constraint

class Celda:
    def __init__(self, tipo, fila, col):
        self.tipo = tipo
        self.fila = fila
        self.col = col
    def __lt__(self, other):
        if isinstance(other, Celda):
            if self.fila == other.fila:
                return self.col < other.col
            else:
                return self.fila < other.fila

    def __str__(self):
        return f'{self.tipo} {self.fila} {self.col}'
    def __repr__(self):
        return self.__str__()

def main(mapa, contenedores):
    problem = constraint.Problem()

    #las variables son cada una de las celdas
    variables = list()
    for i in range(len(mapa)):
        for j in range(len(mapa[0])):
            variables.append(Celda(mapa[i][j], i, j))
    print(variables)

    problem.addVariables(variables, range( 1, len(contenedores)+1 ))

    problem.addConstraint(constraint.AllDifferentConstraint(), variables)

    return problem.getSolutions()

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
        print("Debe introducir: CSPStowage2.py <path> <mapa> <contenedores>")
        quit()
    mapa = read_doc(sys.argv[1], sys.argv[2])        
    contenedores = read_doc(sys.argv[1], sys.argv[3])
    res = main(mapa, contenedores)
    
    print(res)
