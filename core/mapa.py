def calcular_camino_simple(posicion_inicio, posicion_base):
    #genera un camino en linea recta desde una posicion de entrada hasta la base
    #devuelve una lista de posiciones (fila, columna) en orden
    fila, columna = posicion_inicio
    fila_base, columna_base = posicion_base

    camino = [(fila, columna)]
    while (fila, columna) != (fila_base, columna_base):
        if fila < fila_base:
            fila += 1
        elif fila > fila_base:
            fila -= 1
        elif columna < columna_base:
            columna += 1
        elif columna > columna_base:
            columna -= 1
        camino.append((fila, columna))

    return camino
