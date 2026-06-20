from entities import Tower, Unidad, Pared, Base
from data_definitions import TOWERS_CATALOG, UNITS_CATALOG
from combat import CombatEngine
from economy import Economy, DINERO_INICIAL, DINERO_POR_RONDA, RONDAS_PARA_GANAR, HP_BASE, POSICION_BASE, COSTO_PARED, HP_PARED
from data_manager import actualizar_victoria

class Partida:
    def __init__(self, jugador_defensor, jugador_atacante):
        self.jugador_defensor = jugador_defensor
        self.jugador_atacante = jugador_atacante

        self.rondas_defensor = 0
        self.rondas_atacante = 0
        self.ronda_actual = 0

        self.base = Base(hp=HP_BASE, position=POSICION_BASE)
        self.torres = []
        self.paredes = []
        self.unidades = []

        self.economy = Economy()
        self.dinero_defensor = self.economy.dinero_defensor  #referencia directa
        self.dinero_atacante = self.economy.dinero_atacante
        self.victoria_registrada = False

    def iniciar_nueva_ronda(self):
        self.ronda_actual += 1
        self.dinero_defensor = DINERO_INICIAL
        self.dinero_atacante = DINERO_INICIAL

        #limpiar unidades de la ronda anterior, pero mantener torres/paredes/base
        self.unidades = []
        self.torres = [t for t in self.torres if t.esta_vivo()]
        self.paredes = [p for p in self.paredes if p.esta_viva()]

    def comprar_torre(self, tipo, posicion):
        #crea una torre del tipo indicado y la coloca en la posicion dada
        if tipo not in TOWERS_CATALOG:
            return None, "Tipo de torre no existe"
 
        datos = TOWERS_CATALOG[tipo]
        if self.dinero_defensor < datos["coste"]:
            return None, "No tienes suficiente dinero"

        if not self._posicion_libre(posicion):
            return None, "Esa posición ya está ocupada"

        torre = Tower(**datos)
        torre.position = posicion
        self.torres.append(torre)
        self.dinero_defensor -= datos["coste"]
        return torre, f"Torre {torre.nombre} comprada"

    def comprar_pared(self, posicion):
        #crea una pared con costo y HP fijos
        if self.dinero_defensor < COSTO_PARED:
            return None, "No tienes suficiente dinero"

        if not self._posicion_libre(posicion):
            return None, "Esa posición ya está ocupada"

        pared = Pared(coste=COSTO_PARED, hp=HP_PARED)
        pared.position = posicion
        self.paredes.append(pared)
        self.dinero_defensor -= COSTO_PARED
        return pared, "Pared comprada"

    def comprar_unidad(self, tipo, posicion):
        #crea una unidad del tipo indicado y la coloca en la posicion dada
        if tipo not in UNITS_CATALOG:
            return None, "Tipo de unidad no existe"

        datos = UNITS_CATALOG[tipo]
        if self.dinero_atacante < datos["coste"]:
            return None, "No tienes suficiente dinero"

        unidad = Unidad(**datos)
        unidad.position = posicion
        self.unidades.append(unidad)
        self.dinero_atacante -= datos["coste"]
        return unidad, f"Unidad {unidad.nombre} comprada"

    def ejecutar_combate(self):
        motor = CombatEngine(
            towers=self.torres,
            paredes=self.paredes,
            unidades=self.unidades,
            base=self.base,
        )
        frames, resultado = motor.ejecutar_ronda()

        #repartir dinero ganado durante el combate
        self.dinero_defensor += resultado["dinero_defensor"]
        self.dinero_atacante += resultado["dinero_atacante"]

        #actualizar marcador
        if resultado["ganador"] == "defensor":
            self.rondas_defensor += 1
        else:
            self.rondas_atacante += 1

        return frames, resultado

    def hay_ganador_partida(self):#devuelve el nombre del ganador si alguien llego a 3 rondas, o None si sigue el juego
        if self.base.esta_destruida():
            if not self.victoria_registrada:
                actualizar_victoria(self.jugador_atacante, "atacante")
                self.victoria_registrada = True
            return self.jugador_atacante
    
        if self.rondas_defensor >= RONDAS_PARA_GANAR:
            if not self.victoria_registrada:
                actualizar_victoria(self.jugador_defensor, "defensor")
                self.victoria_registrada = True
            return self.jugador_defensor

        if self.rondas_atacante >= RONDAS_PARA_GANAR:
            if not self.victoria_registrada:
                actualizar_victoria(self.jugador_atacante, "atacante")
                self.victoria_registrada = True
            return self.jugador_atacante

        return None
    
    def obtener_catalogo_torres(self):
        #para que la UI muestre las opciones de compra del defensor
        return TOWERS_CATALOG
 
    def obtener_catalogo_unidades(self):
        #para que la UI muestre las opciones de compra del atacante
        return UNITS_CATALOG
 
    def obtener_estado(self):
        #resumen del estado actual de la partida, util para la UI
        return {
            "ronda_actual": self.ronda_actual,
            "rondas_defensor": self.rondas_defensor,
            "rondas_atacante": self.rondas_atacante,
            "dinero_defensor": self.dinero_defensor,
            "dinero_atacante": self.dinero_atacante,
            "base_hp": self.base.hp,
            "torres_vivas": len(self.torres),
            "paredes_vivas": len(self.paredes),
            "unidades_activas": len(self.unidades),
        }
 
    def _posicion_libre(self, posicion):#verifica que no haya ya una torre, pared o la base en esa posicion
        ocupadas = [t.position for t in self.torres]
        ocupadas += [p.position for p in self.paredes]
        ocupadas.append(self.base.position)
        return posicion not in ocupadas