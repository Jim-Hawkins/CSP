import sys
import constraint

class Problema:
    """ Clase que representa al problema. Contiene variables, dominios
        y restricciones. Recibe el esquema del barco y la lista de contenedores """
    def __init__(self, mapa, contenedores):

        # dominio para contenedores refrigerados y normales
        self.dom_r = list()
        self.dom_s = list()
        for nivel in range(len(mapa)):
            for pila in range(len(mapa[nivel])):
                celda = mapa[nivel][pila]
                if celda != "X":   # Tanto si es N como E, añadimos al dominio de los normales
                    self.dom_s.append( (pila, nivel) )
                if celda == "E":   # Solo si es E, añadimos al dominio de los refrigerados
                    self.dom_r.append( (pila, nivel) )
        

        # Creamos la variable 'profundidades' para ver la profundidad real del 
        # barco, es decir, hasta donde hay una X, que representa la base
        self.profundidades = list()
        for pila in range(len(mapa[0])):
            nivel = 0
            while nivel < len(mapa) and mapa[nivel][pila] != "X":
                nivel += 1
            self.profundidades.append(nivel-1)

        # Creamos un objeto problema
        self.problem = constraint.Problem()

        # Lista con las variables
        self.variables = list(range(1, len(contenedores) + 1))

        # Lista con el puerto al que va cada contenedor
        self.puertos = list()

        # add las variables con sus correspondientes dominios
        for i in range(len(contenedores)):
            if contenedores[i][1] == "S":
                self.problem.addVariable(i+1, self.dom_s)
            elif contenedores[i][1] == "R":
                self.problem.addVariable(i+1, self.dom_r)

            self.puertos.append(contenedores[i][2])

        # Restricciones del problema
        self.problem.addConstraint(constraint.AllDifferentConstraint(), self.variables)
        for i in range(1, len(contenedores) + 1):
            for j in range(1, len(contenedores) + 1):
                if i != j:
                    self.problem.addConstraint(self.constraint_uno_debajo_de_otro, [i, j])
                #self.problem.addConstraint(self.puertos,  [i, j])
                pass

    def solve(self):
        ''' Metodo para la resolucion final del problema '''
        return self.problem.getSolutions()

    def constraint_uno_debajo_de_otro(self, a, b):
        # a = uno, b = otro
        #print(a, b)
        # a = (0,0) b = (0,0)
        # a = (0,0) b = (0,1)
        # a = (0,3) b = (0,2)
        # a = (2,3) b = (2,2)
        #if a==(2,3) and b == (2,2): print((a[1] == self.profundidades[a[0]] or ( (a[0] == b[0]) and ( a[1] - b[1] == 1 ) )), ".......................")
        return (a[1] == self.profundidades[a[0]] or ( ( (a[0] == b[0]) and abs(a[1] - b[1]) == 1 ) ) )

    def puertos(varA, varB):
        def innerFunction(a, b):
            return ( (a[0] != b[0])
                     or ( a[1] < b[1]
                         and self.puertos[varA-1] == "2"
                         and self.puertos[varB-1] == "2" 
                        )
                    )
        return innerFunction(varA, varB)

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
    '''try:
        res = Problema(mapa, contenedores).solve()
    except Exception as e:
        print(e)'''

    res = Problema(mapa, contenedores).solve()
    
    # escribimos el resultado en el documento de salida especificado
    with open(f'{sys.argv[1]}/{sys.argv[2]}-{sys.argv[3]}.output', 'w', encoding="UTF-8") as outfile:
        outfile.write("Número de soluciones: {}\n".format(len(res)))
        for d in res:
            outfile.write(str(d) + "\n")
