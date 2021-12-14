contenedores = 
    [
        ['1S1'],
        ['2S1'],
        ['3S2'],
        ['4R1'],
        ['5R2'],
    ]
posiciones = 
    [
        ['N(0,0)'],
        ['N(0,1)'],
        ['N(1,0)'],
        ['E(1,1)'],
        ['E(1,2)'],
        ['N(1,3)'],
    ]
soluciones = []
abierta = [contenedores.copy()]
cerrada = []

parada = False

while not parada:
    #Paso0.1
    mas_profundas = busca_max_profundidad(posiciones)
    #Paso0.2
    conten_act = abierta.pop(0)
    for p in mas_profundas:                    
        for c in conten_act:
            if p.tipo == "E":
                c.append(p)
            if p.tipo == "N" and c.tipo == "S":
                c.append(p)
     #Paso1
     for c in range(len(conten_act)):
        if len(conten_act[c]) > 1:    # si hay alguna posible asignación para c
            for p in range(1, len(conten_act[c])-1):
                costes.append( ( (c, p), busca_f(conten_act[c][0], conten_act[c][p])) )
            
     

