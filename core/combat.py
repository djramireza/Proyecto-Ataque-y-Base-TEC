from entities import Tower, Unidad, Pared, Base
from economy import BONUS_DESTRUIR_ESTRUCTURA, BONUS_ELIMINAR_UNIDAD

MAX_TURNOS_POR_DEFECTO = 120


class CombatEngine:
    def __init__(self, towers, paredes, unidades, base):#recibe listas de objetos: torres, paredes, unidades, y el objeto base
        self.towers = towers
        self.paredes = paredes
        self.unidades = unidades
        self.base = base
        self.turno_actual = 0
        self.dinero_defensor_ganado = 0
        self.dinero_atacante_ganado = 0
        self.frames = []

        for torre in self.towers:
            torre.lista = False
            torre.turnos_boost_restantes = 0

        # Acumulador de movimiento: una unidad con velocidad 0.5 avanza una celda
        # cada dos turnos, una con velocidad 2 avanza dos celdas por turno, etc.
        for unidad in self.unidades:
            unidad.movimiento_acumulado = 0.0
            unidad.lista = False

    def ejecutar_ronda(self, max_turnos=MAX_TURNOS_POR_DEFECTO):
        #ejecuta turnos hasta que termine el combate y devuelve (frames, resultado)
        #frames es una lista de snapshots (uno por turno) para que la UI anime el combate
        self.frames = [self._snapshot()]

        while self.turno_actual < max_turnos:
            self.turno_actual += 1

            self._fase_torres()
            self._fase_unidades()

            self.frames.append(self._snapshot())

            if self._todas_unidades_muertas():
                return self.frames, self._resultado("defensor")

            if self.base.esta_destruida():
                return self.frames, self._resultado("atacante")

        return self.frames, self._resultado("defensor")

    def _distancia(self, pos1, pos2):#distancia simple entre dos casillas (fila, columna)
        if pos1 is None or pos2 is None:
            return 999
        return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])

    def _buscar_unidad_en_rango(self, torre):#devuelve la primera unidad viva dentro del rango de la torre
        for unidad in self.unidades:
            if unidad.esta_vivo() and self._distancia(torre.position, unidad.position) <= torre.rango:
                return unidad
        return None

    def _obstaculo_en_celda(self, posicion):#devuelve la primera torre o pared viva en esa celda exacta
        for obstaculo in self.towers + self.paredes:
            if self._esta_vivo(obstaculo) and obstaculo.position == posicion:
                return obstaculo
        return None

    def _esta_vivo(self, objeto):#Tower y Unidad usan esta_vivo(), Pared usa esta_viva()
        if hasattr(objeto, "esta_vivo"):
            return objeto.esta_vivo()
        return objeto.esta_viva()

    def _fase_torres(self):#cada torre viva ataca a la unidad más cercana dentro de su rango
        for torre in self.towers:
            if not torre.esta_vivo():
                torre.lista = False
                continue

            if torre.turnos_boost_restantes > 0:
                torre.turnos_boost_restantes -= 1
                if torre.turnos_boost_restantes == 0:
                    torre.daño = int(torre.daño / 1.2)

            torre.avanzar_cooldown()

            objetivo = self._buscar_unidad_en_rango(torre)
            if objetivo:
                if torre.puede_usar_habilidad():
                    self._usar_habilidad_torre(torre, objetivo)
                    torre.resetear_cooldown()
                    torre.lista = True
                else:
                    objetivo.recibir_daño(torre.daño)
                    torre.lista = False

                if not objetivo.esta_vivo():
                    self.dinero_defensor_ganado += self._valor_unidad(objetivo)
            else:
                torre.lista = False

    def _usar_habilidad_torre(self, torre, objetivo):
        if torre.habilidad == "disparo_doble":
        # Básica: dispara con el doble de daño en ese golpe
            objetivo.recibir_daño(torre.daño * 2)

        elif torre.habilidad == "boost_temporal":
        # Pesada: sube su daño 20% por 3 turnos, luego vuelve a la normalidad.
        # Si se vuelve a activar mientras el boost ya esta activo, solo se le
        # renueva la duracion (NO se vuelve a multiplicar el daño otra vez,
        # sino el daño se iba a triplicar y cuadruplicar sin parar).
            if torre.turnos_boost_restantes == 0:
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

    def _fase_unidades(self):#cada unidad viva avanza segun su velocidad, o ataca lo que tenga adelante
        base_col = self.base.position[1]

        for unidad in self.unidades:
            if not unidad.esta_vivo():
                continue

            unidad.lista = False  # se vuelve a marcar True solo si usa su habilidad este turno
            unidad.movimiento_acumulado += unidad.velocidad

            # Una unidad puede avanzar varias celdas en el mismo turno si su velocidad
            # es mayor a 1 (ej. velocidad 2 = dos celdas); si encuentra un obstaculo o
            # llega a la base, ataca y el resto del movimiento de este turno se pierde.
            while unidad.movimiento_acumulado >= 1 and unidad.esta_vivo():
                fila, columna = unidad.position

                if columna >= base_col:
                    objetivo = None  # ya llegó a la columna de la base: la ataca directamente
                else:
                    objetivo = self._obstaculo_en_celda((fila, columna + 1))

                if objetivo is None and columna < base_col:
                    unidad.position = (fila, columna + 1)
                    unidad.movimiento_acumulado -= 1
                    continue

                unidad.avanzar_cooldown()

                if unidad.puede_usar_habilidad():
                    self._usar_habilidad_unidad(unidad, objetivo)
                    unidad.resetear_cooldown()
                    unidad.lista = True
                else:
                    self._atacar_normal(unidad, objetivo, unidad.daño)

                unidad.movimiento_acumulado = 0
                break

    def _usar_habilidad_unidad(self, unidad, objetivo):
        if unidad.habilidad == "ataque_doble":
            # Regular: ataca con el doble de daño
            self._atacar_normal(unidad, objetivo, unidad.daño * 2)

        elif unidad.habilidad == "escudo":#Heavy: activa escudo temporal (recibe la mitad del daño)
            unidad.shield_activo = True
            self._atacar_normal(unidad, objetivo, unidad.daño)

        elif unidad.habilidad == "ataque_doble_rapido":
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

            # El atacante solo gana dinero por dañar/destruir torres o la base, no por
            # golpear muros (los muros son solo bloqueo barato, no le dan plata a nadie).
            if not isinstance(objetivo, Pared):
                self.dinero_atacante_ganado += daño
                if estaba_vivo_antes and not self._esta_vivo(objetivo):
                    self.dinero_atacante_ganado += BONUS_DESTRUIR_ESTRUCTURA

    def _todas_unidades_muertas(self):
        return all(not u.esta_vivo() for u in self.unidades)

    def _valor_unidad(self, unidad):#dinero que gana el defensor por eliminar esta unidad
        return int(unidad.coste * BONUS_ELIMINAR_UNIDAD)

    def _snapshot(self):#una "foto" del estado actual, en el mismo formato que espera ui/combat_view.py
        torres = []
        for t in self.towers:
            torres.append({
                "tipo": getattr(t, "tipo", None),
                "posicion": t.position,
                "hp": t.hp,
                "hp_max": t.max_hp,
                "cooldown": t.cooldown_actual,
                "lista": getattr(t, "lista", False),
            })

        muros = []
        for p in self.paredes:
            muros.append({
                "posicion": p.position,
                "hp": p.hp,
                "hp_max": p.max_hp,
            })

        unidades = []
        for u in self.unidades:
            if u.esta_vivo():
                unidades.append({
                    "tipo": getattr(u, "tipo", None),
                    "etiqueta": getattr(u, "etiqueta", "UNI"),
                    "posicion": u.position,
                    "hp": u.hp,
                    "hp_max": u.max_hp,
                    "lista": getattr(u, "lista", False),
                })

        return {"torres": torres, "muros": muros, "unidades": unidades, "base_hp": self.base.hp}

    def _resultado(self, ganador):
        return {"ganador": ganador, "turnos": self.turno_actual, "dinero_defensor": self.dinero_defensor_ganado,
            "dinero_atacante": self.dinero_atacante_ganado,"base_hp_restante": self.base.hp,}
