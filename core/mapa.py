FILAS = 10
COLUMNAS = 10
 
VACIO = "vacio"
TORRE = "torre"
PARED = "pared"
BASE = "base"
 
 
class Mapa:
    def __init__(self, posicion_base):
        # crea una grilla de FILAS x COLUMNAS, todas vacias al inicio
        self.filas = FILAS
        self.columnas = COLUMNAS
        self.grid = [[VACIO for _ in range(COLUMNAS)] for _ in range(FILAS)]
        self.posicion_base = posicion_base
        self._marcar(posicion_base, BASE)
 
    def _marcar(self, posicion, tipo):
        fila, columna = posicion
        self.grid[fila][columna] = tipo
 
    def posicion_valida(self, posicion):#revisa que la posicion este dentro de los limites del mapa
        fila, columna = posicion
        return 0 <= fila < self.filas and 0 <= columna < self.columnas
 
    def posicion_libre(self, posicion):#revisa que la posicion este dentro del mapa y este vacia
        if not self.posicion_valida(posicion):
            return False
        fila, columna = posicion
        return self.grid[fila][columna] == VACIO
 
    def colocar_torre(self, posicion):
        if not self.posicion_libre(posicion):
            return False, "Posición inválida u ocupada"
        self._marcar(posicion, TORRE)
        return True, "Torre colocada"
 
    def colocar_pared(self, posicion):
        if not self.posicion_libre(posicion):
            return False, "Posición inválida u ocupada"
        self._marcar(posicion, PARED)
        return True, "Pared colocada"
 
    def liberar_posicion(self, posicion):#se usa cuando una torre o pared es destruida, para liberar la casilla
        if self.posicion_valida(posicion) and posicion != self.posicion_base:
            self._marcar(posicion, VACIO)
 
    def obtener_contenido(self, posicion):
        if not self.posicion_valida(posicion):
            return None
        fila, columna = posicion
        return self.grid[fila][columna]
 
    def obtener_grid_completo(self):#devuelve la grilla completa, util para que la UI la dibuje
        return self.grid
 
    def calcular_camino_simple(self, posicion_inicio):#genera un camino en linea recta desde una posicion de entrada hasta la base
                                                      #devuelve una lista de posiciones (fila, columna) en orden
        fila, columna = posicion_inicio
        fila_base, columna_base = self.posicion_base
 
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
    
    