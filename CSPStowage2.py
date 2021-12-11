import sys
import constraint
import time

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
        else:
            return self.fila < other

    def __str__(self):
        return f'{self.tipo} {self.fila} {self.col}'
    def __repr__(self):
        return self.__str__()

class container:

    def __init__(self, tipo, id, destino):
        self.tipo = tipo
        self.id = id
        self.destino = destino
    
    def __str__(self):
        return f'{self.tipo} {self.id} {self.destino}'

    def __repr__(self):
        return self.__str__()

def main(mapa, contenedores):
    # Forzamos a que haya por lo menos tantos contenedores como celdas,
    # para permitir una asignación total. Al mismo tiempo, forzamos a 
    # que haya suficientes celdas para todos los contenedores 
    if len(contenedores) != contar_celdas(mapa):
        print("Debe haber tantas celdas como contenedores")
        return

    # Comprobamos que haya suficientes celdas E para los contenedores R
    if contar_celdas(mapa, "E") < contar_contenedores(contenedores, "R"):
        print("No hay suficientes celdas electrificadas")
        return

    # Las variables son cada una de las celdas
    variables = list()
    for i in range(len(mapa)):
        for j in range(len(mapa[i])):
            #variables.append(Celda(mapa[i][j], i, j))
            variables.append(f'{mapa[i][j]}{i}{j}')

    dominios = list()
    for i in contenedores:
        dominios.append(container(i[1],i[0],i[2]))
    
    problem = constraint.Problem()
        
    '''
    for i in range(len(contenedores)):
        print(dominios[i])
    '''

    print(variables, contenedores)
    #problem.addVariables(variables, dominios)
    problem.addVariables(variables, contenedores)
    problem.addConstraint(constraint.AllDifferentConstraint(), variables)
    for i in variables:
        problem.addConstraint(c_celda_refrg, i)
    return problem.getSolutions()

def c_celda_refrg(var):
    def innerFunction(value):
        return "E" == var.tipo and "R" == value.tipo
    return innerFunction

def contar_contenedores(lista, tipo):
    contador = 0
    for cont in lista:
        if tipo in cont:
            contador += 1
    return contador

def contar_celdas(lista_de_listas, tipo=""):
    contador = 0
    for fila in lista_de_listas:
        for c in fila:
            if tipo in c:
                contador += 1
    return contador

def removeX(lista):
    res = list()
    for i in lista:
        if i != "X":
            res.append(i)
    return res

def read_doc(path, file):
    res = list()
    with open(path + "/" + file) as infile:
        lectura = infile.readline()
        lectura = lectura.split(" ")
        lectura[-1] = lectura[-1].replace("\n", "")
        lectura = removeX(lectura)
        while len(lectura) >= 1:
            res.append(lectura)
            lectura = infile.readline()
            lectura = lectura.split(" ")
            lectura[-1] = lectura[-1].replace("\n", "")
            lectura = removeX(lectura)
            #time.sleep(1)
            #print(res)
    return res

def read_doc_container(path, file):
    res = []
    with open(path + "/" + file) as infile:
        lectura = infile.readline()
        lectura = lectura.replace(" ", "")
        lectura = lectura.replace("\n", "")
        while lectura:
            res.append(lectura)
            lectura = infile.readline().replace(" ", "")
            lectura = lectura.replace("\n", "")
    return res

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Debe introducir: CSPStowage2.py <path> <mapa> <contenedores>")
        quit()
    mapa = read_doc(sys.argv[1], sys.argv[2])        
    contenedores = read_doc_container(sys.argv[1], sys.argv[3])
    res = main(mapa, contenedores)
    
    print(res)
