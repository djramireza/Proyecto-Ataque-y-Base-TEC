from entities import Tower, Unidad, Pared, Base
 
MAX_TURNOS = 3
 
 
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

            if hasattr(torre, "turnos_boost_restantes") and torre.turnos_boost_restantes > 0:
                torre.turnos_boost_restantes -= 1
                if torre.turnos_boost_restantes == 0:
                    torre.daño = int(torre.daño / 1.2)

            torre.avanzar_cooldown()

            objetivo = self._buscar_unidad_en_rango(torre)
            if objetivo:
                if torre.puede_usar_habilidad():
                    self._usar_habilidad_torre(torre, objetivo)
                    torre.resetear_cooldown()
                else:
                    objetivo.recibir_daño(torre.daño)

                if not objetivo.esta_vivo():
                    self.dinero_defensor_ganado += self._valor_unidad(objetivo)

    def _usar_habilidad_torre(self, torre, objetivo):
        if torre.habilidad == "disparo_doble":
        # Básica: dispara con el doble de daño en ese golpe
            objetivo.recibir_daño(torre.daño * 2)

        elif torre.habilidad == "boost_temporal":
        # Pesada: sube su daño 20% por 3 turnos, luego vuelve a la normalidad
            torre.daño = int(torre.daño * 1.2)
            torre.turnos_boost_restantes = 3
            objetivo.recibir_daño(torre.daño)

        elif torre.habilidad == "curar_torre":
        # Mágica: busca otra torre con HP menor al máximo y la cura al 100%
            for otra_torre in self.towers:
                if otra_torre is not torre and otra_torre.esta_vivo() and otra_torre.hp < otra_torre.max_hp:
                    otra_torre.hp = otra_torre.max_hp
                    break
            objetivo.recibir_daño(torre.daño)
 
    def _fase_unidades(self):#cada unidad viva avanza, ataca torres/paredes en su camino, o daña la base
        for unidad in self.unidades:
            if not unidad.esta_vivo():
                continue
 
            unidad.avanzar_cooldown()
 
            objetivo = self._buscar_obstaculo_en_camino(unidad)
 
            if unidad.puede_usar_habilidad():
                self._usar_habilidad_unidad(unidad, objetivo)
                unidad.resetear_cooldown()
            else:
                self._atacar_normal(unidad, objetivo, unidad.daño)

 
    def _usar_habilidad_unidad(self, unidad, objetivo):
        if unidad.habilidad == "ataque_doble":
            # Regular: ataca con el doble de daño
            self._atacar_normal(unidad, objetivo, unidad.daño * 2)
 
        elif unidad.habilidad == "escudo":#Heavy: activa escudo temporal (recibe la mitad del daño)
            unidad.shield_activo = True
            self._atacar_normal(unidad, objetivo, unidad.daño)
 
        elif unidad.habilidad == "aumento_velocidad":
            # Fast: ataca dos veces en el mismo turno
            self._atacar_normal(unidad, objetivo, unidad.daño)
            if unidad.esta_vivo():
                self._atacar_normal(unidad, objetivo, unidad.daño)
 
        else:
            # fallback por si llega una habilidad no reconocida
            self._atacar_normal(unidad, objetivo, unidad.daño)

    def _atacar_normal(self, unidad, objetivo, daño):
        if objetivo is None:#no hay obstaculo en el camino entonces daña la base directamente
            self.base.recibir_daño(daño)
            self.dinero_atacante_ganado += daño
        else:
            estaba_vivo_antes = self._esta_vivo(objetivo)
            objetivo.recibir_daño(daño)
            self.dinero_atacante_ganado += daño
 
            if estaba_vivo_antes and not self._esta_vivo(objetivo):
                self.dinero_atacante_ganado += 20

    def _todas_unidades_muertas(self):
        return all(not u.esta_vivo() for u in self.unidades)
 
    def _valor_unidad(self, unidad):#dinero que gana el defensor por eliminar esta unidad
        return unidad.coste // 2
 
    def _resultado(self, ganador):
        return {"ganador": ganador, "turnos": self.turno_actual, "dinero_defensor": self.dinero_defensor_ganado,
            "dinero_atacante": self.dinero_atacante_ganado,"base_hp_restante": self.base.hp,}