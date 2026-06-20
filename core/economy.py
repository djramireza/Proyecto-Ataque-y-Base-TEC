DINERO_INICIAL = 200
DINERO_POR_RONDA = 100
RONDAS_PARA_GANAR = 3
HP_BASE = 300
POSICION_BASE = (4, 14)
COSTO_PARED = 10
HP_PARED = 40

BONUS_DESTRUIR_ESTRUCTURA = 20  
BONUS_ELIMINAR_UNIDAD = 0.5

class Economy:
    def __init__(self):
        self.dinero_defensor = DINERO_INICIAL
        self.dinero_atacante = DINERO_INICIAL

    def nueva_ronda(self):#suma dinero fijo al inicio de cada ronda
        self.dinero_defensor += DINERO_POR_RONDA
        self.dinero_atacante += DINERO_POR_RONDA

    def cobrar_defensor(self, costo):#descuenta dinero al defensor, devuelve True si pudo pagar
        if self.dinero_defensor < costo:
            return False
        self.dinero_defensor -= costo
        return True

    def cobrar_atacante(self, costo):#descuenta dinero al atacante, devuelve True si pudo pagar
        if self.dinero_atacante < costo:
            return False
        self.dinero_atacante -= costo
        return True

    def ganar_defensor(self, cantidad):#el defensor gana dinero por eliminar unidades
        self.dinero_defensor += cantidad

    def ganar_atacante(self, cantidad):#el atacante gana dinero por dañar torres o la base
        self.dinero_atacante += cantidad

    def calcular_ganancia_por_unidad(self, costo_unidad):#el defensor gana la mitad del costo de la unidad eliminada
        return int(costo_unidad * BONUS_ELIMINAR_UNIDAD)

    def obtener_estado(self):
        return {
            "dinero_defensor": self.dinero_defensor,"dinero_atacante": self.dinero_atacante}