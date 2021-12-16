for m in {1..8}
do
    for c in {1..3} 
    do
        echo mapa$m contenedores$c
        python CSPStowage.py CSP-tests mapa$m contenedores$c
    done
done
