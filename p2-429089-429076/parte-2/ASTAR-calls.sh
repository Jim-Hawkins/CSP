for m in {1..7}
do
    for c in {1..4}
    do
        for h in {1..2}
        do
            python ASTARStowage.py mapa$m contenedores$c $h &
        done
    done
done