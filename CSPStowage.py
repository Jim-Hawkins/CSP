import sys
import constraint

def main(mapa, contenedores):

    problem = constraint.Problem()
    
    problem.addVariables( [i[0] for i in contenedores], ( range(len(mapa)) ) )
    
    problem.addConstraint()
    return


if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Debe introducir: CSPStowage.py <path> <mapa> <contenedores>")
    else:
        mapa = []
        with open(sys.argv[1] + "/" + sys.argv[2]) as map_file:
            lectura = map_file.readline().split(" ")
            lectura[-1] = lectura[-1].replace("\n", "")
            while len(lectura) != 1:
                mapa.append(lectura)
                lectura = map_file.readline().split(" ")
                lectura[-1] = lectura[-1].replace("\n", "")
            
        contenedores = []
        with open(sys.argv[1] + "/" + sys.argv[3]) as container_file:
            lectura = container_file.readline().split(" ")
            lectura[-1] = lectura[-1].replace("\n", "")
            while len(lectura) != 1:
                contenedores.append(lectura)
                lectura = container_file.readline().split(" ")
                lectura[-1] = lectura[-1].replace("\n", "")

        res = main(mapa, contenedores)
        
        print(res)
