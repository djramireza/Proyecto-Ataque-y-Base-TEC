from entities import Tower, Unidad, Pared, Base

max_turnos = 4

class CombatEngine:
    def __init__(self, towers, paredes, unidades, base): #reccibe una lista de objetos, asi sean torres,
        self.towers = towers                             # paredes, unidades y la base
        self.pared = paredes
        self.unidades = unidades
        self.base = base
        self.turno_actual = 0
        self.dinero_defensor_ganado = 0
        self.dinero_atacante_ganado = 0

    def ejecutrar_ronda(self): #ejectua los turnoshasta que termine el combate y tira el resultado
        while self.turno_actual < max_turnos:
            self.turno_actual += 1

            self.fase_torres()
            self.fase_unidades()

            if self._todas_unidades_muertas():
                return self._resultado("defensor")
        
            if self.base.esta_destruida():
                return self._resultado("atacante")
        
        return self._resultado("defensor")
    
    def _distancia(self, pos1, pos2): #distancia simple entre dos casillas
        if pos1 is None or pos2 is None:
            return 999
        return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])

    def _buscar_unidad_en_rango(self, torre): #devuelve la primera unidad viva dentro del rango de la torre
        for unidad in self.units:
            if unidad.esta_viva() and self._distancia(torre.position, unidad.position) <= torre.range:
                return unidad
            
        return None
    
    def _buscar_obstaculo_en_camino(self, unidad):# deveulve la primera torre o muro vivo en el camino
        for obstaculo in self.towers + self.walls:
            if obstaculo.esta_viva() and self._distancia(obstaculo.position, unidad.position) <= 1:
                return obstaculo
        return None
    
    def _fase_torres(self): #cada torre viva ataca a la unidad ms cercana de su rango
        for torre in self.towers:
            if not torre.esta_viva():
                continue

            torre.avanzar_cooldown()

            objetivo = self._buscar_unidad_en_rango(torre)
            if objetivo:
                torre.use_Ability_if_ready(objetivo) if hasattr (torre, "use_ability_if_ready") else None
                objetivo.recibir_daño(torre.damage)

            if not objetivo.esta_vivo():
                self.dinero_defensor_ganado += self._valor_unidad(objetivo)

    def _fase_unidades(self):#cada unidad viva avanza, ataca torres o muros en su camino
        for unidad in self.unidades:
            if not unidad.esta_viva():
                continue
            unidad.avanzar_cooldown() 

            objetivo = self._buscar_obstaculo_en_camino(unidad) 

            if objetivo is None:
                self.bse.recibir_daño(unidad.damage)
                self.dinero_atacante_ganado += unidad.damage
            else:
                objetivo.recibir_daño(unidad.damage)
                self.dinero_atacante_ganado +=unidad.damage

                if hasattr(objetivo, "esta vivo") and not objetivo.esta_vivo():
                    self.dinero_atacante_ganado += 20 #bonus por haber destruido torre o muro
            
    def _todas_unidades_muertas(self):
        return all(not u.esta_vivo() for u in self.unidades)
    
    def _valor_unidad(self, unidad): #dinero que gana el defensor por eliminar esta unidad
        return unidad.cost // 2
    
    def resultado(self, ganador):
        return {"ganador": ganador, "turnos": self.turno_actual, "dinero_defensor": self.dinero_defensor_ganado,
                "dinero_atacante": self.dinero_atacante_ganado, "base_hp_restante": self.base.hp}