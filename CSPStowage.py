import sys
import constraint

def main(mapa, contenedores):

    variables = list()
    for i in contenedores:
        variables.append(i[0])

    problem = constraint.Problem()

    problem.addVariables(
                         variables,
                         range(len(mapa) * len(mapa[0]))
                        )

    prohibidos = encuentra_celdas(contenedores, "X")
    electrificados = encuentra_celdas(contenedores, "E")
    '''problem.addConstraint(constraint_refrigerados, 
                          (variables, electrificados))
    problem.addConstraint(constraint_prohibidos, 
                          (variables, prohibidos))
                          '''
    problem.addConstraint(constraint_contenedores_ordenados, 
                          variables)
    '''
    problem.addConstraint(constraint_suficientes_celdas, 
                          (mapa, contenedores, "E", "R"))
    problem.addConstraint(constraint_suficientes_celdas, 
                          (mapa, contenedores, "N", "S"))'''
    return problem.getSolutions()

def encuentra_celdas(contenedores, tipo):
    res = list()
    for i in range(len(contenedores)):
        for j in range(len(contenedores[0])):
            if contenedores[i][j] == tipo:
                res.append( i*len(contenedores[0]) + j )
    return res

def constraint_refrigerados(cont, electrificados):
    return cont in electrificados

def constraint_prohibidos(cont, prohibidos):
    return cont not in prohibidos

def constraint_contenedores_ordenados(*args):
    ''' Los contenedores que van al puerto 1 deben estar por encima
        de los del puerto 2'''
    print(args[0])
    '''
    for contA in range(len(args)):
        for contB in range(contA+1,len(args)):
            if contA != contB and contA!=contB:
                print(contA, contB)
                print("---------------")
                print(contenedores)
                # obtenemos el destino de cada contenedor
                for fila in contenedores:
                    if contenedores[contA][0] in fila:
                        destA = fila[2]
                    if contenedores[contB][0] in fila:
                        destB = fila[2]

            if destA == destB: return True
            if destA == 1: return destA > destB
    '''
                

def constraint_suficientes_celdas(mapa, contenedores, tipo_celda, tipo_cont):
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

def constraint_gravedad():
    pass


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
    res = main(mapa, contenedores)
    
    print(res)
