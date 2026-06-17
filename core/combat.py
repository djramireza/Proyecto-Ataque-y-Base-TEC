from entities import Tower, Unidad, Pared, Base
 
MAX_TURNOS = 4
 
 
class CombatEngine:
    def __init__(self, towers, paredes, unidades, base):#recibe listas de objetos: torres, paredes, unidades, y el objeto base
        self.towers = towers
        self.paredes = paredes
        self.unidades = unidades
        self.base = base
        self.turno_actual = 0
        self.dinero_defensor_ganado = 0
        self.dinero_atacante_ganado = 0
 
    def ejecutar_ronda(self):#ejecuta turnos hasta que termine el combate y devuelve el resultado
        while self.turno_actual < MAX_TURNOS:
            self.turno_actual += 1
 
            self._fase_torres()
            self._fase_unidades()
 
            if self._todas_unidades_muertas():
                return self._resultado("defensor")
 
            if self.base.esta_destruida():
                return self._resultado("atacante")
 
        return self._resultado("defensor")
 
    def _distancia(self, pos1, pos2):#distancia simple entre dos casillas (fila, columna)
        if pos1 is None or pos2 is None:
            return 999
        return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])
 
    def _buscar_unidad_en_rango(self, torre):#devuelve la primera unidad viva dentro del rango de la torre
        for unidad in self.unidades:
            if unidad.esta_vivo() and self._distancia(torre.position, unidad.position) <= torre.rango:
                return unidad
        return None
 
    def _buscar_obstaculo_en_camino(self, unidad):#devuelve la primera torre o pared viva en el camino de la unidad
        for obstaculo in self.towers + self.paredes:
            if self._esta_vivo(obstaculo) and self._distancia(obstaculo.position, unidad.position) <= 1:
                return obstaculo
        return None
 
    def _esta_vivo(self, objeto):#Tower y Unidad usan esta_vivo(), Pared usa esta_viva()
        if hasattr(objeto, "esta_vivo"):
            return objeto.esta_vivo()
        return objeto.esta_viva()
 
    def _fase_torres(self):#cada torre viva ataca a la unidad más cercana dentro de su rango
        for torre in self.towers:
            if not torre.esta_vivo():
                continue
 
            torre.avanzar_cooldown()
 
            objetivo = self._buscar_unidad_en_rango(torre)
            if objetivo:
                objetivo.recibir_daño(torre.daño)
 
                if not objetivo.esta_vivo():
                    self.dinero_defensor_ganado += self._valor_unidad(objetivo)
 
    def _fase_unidades(self):#cada unidad viva avanza, ataca torres/paredes en su camino, o daña la base
        for unidad in self.unidades:
            if not unidad.esta_vivo():
                continue
 
            unidad.avanzar_cooldown()
 
            objetivo = self._buscar_obstaculo_en_camino(unidad)
 
            if objetivo is None:
                self.base.recibir_daño(unidad.daño)
                self.dinero_atacante_ganado += unidad.daño
            else:
                estaba_vivo_antes = self._esta_vivo(objetivo)
                objetivo.recibir_daño(unidad.daño)
                self.dinero_atacante_ganado += unidad.daño
 
                if estaba_vivo_antes and not self._esta_vivo(objetivo):
                    self.dinero_atacante_ganado += 20  # bonus por destruir torre o pared
 
    def _todas_unidades_muertas(self):
        return all(not u.esta_vivo() for u in self.unidades)
 
    def _valor_unidad(self, unidad):#dinero que gana el defensor por eliminar esta unidad
        return unidad.coste // 2
 
    def _resultado(self, ganador):
        return {"ganador": ganador, "turnos": self.turno_actual, "dinero_defensor": self.dinero_defensor_ganado,
            "dinero_atacante": self.dinero_atacante_ganado,"base_hp_restante": self.base.hp,}