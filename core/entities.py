class Tower:
    def __init__(self, nombre, costo, hp, daño, rango, habilidad, cooldown):
        self.nombre = nombre
        self.costo = costo
        self.hp = hp
        self.daño = daño
        self.rango = rango
        self.habilidad = habilidad
        self.cooldown = cooldown #turnos para activar habilidad 
        self.copoldown_actual = 0 
        self.position = None # va a ser fila, columna

    def esta_vivo(self): 
        return self.hp > 0
    
    def recibir_daño(self, cantidad):
        self.hp -= cantidad
        if self.hp <0:
            self.hp = 0

    def puede_usar_habilidad(self):
        return self.cooldown_actual >= self.cooldown
    
    def resetear_cooldown(self):
        cooldown_actual = 0

    def avanzar_cooldown(self):
        if self.copoldown_actual < self.cooldown:
            self.copoldown_actual += 1

class Unidad:
    def __init__(self, nombre, coste, hp, daño, velocidad, habilidad, cooldown):
        self.nombre = nombre
        self.coste = coste
        self.hp = hp
        self.daño = daño
        self.velocidad = velocidad
        self.habilidad = habilidad
        self.cooldown = cooldown
        self.cooldown_actual = 0
        self.position = None
        self.shield_activo = False
    
    def esta_vivo(self):
        return self.hp > 0
    
    def recibir_daño(self, cantidad):
        if self.shield_activo:
            cantidad = cantidad // 2  #ejemplo de reducción por escudo
            self.shield_activo = False
        self.hp -= cantidad
        if self.hp < 0:
            self.hp = 0

    def puede_usar_habilidad(self):
        return self.cooldown_actual >= self.cooldown

    def resetear_cooldown(self):
        self.cooldown_actual = 0

    def avanzar_cooldown(self):
        if self.cooldown_actual < self.cooldown:
            self.cooldown_actual += 1

class Pared:
    def __init__(self, costo, hp):
        self.costo = costo
        self.hp = hp
        self.position = None
        
    def esta_viva(self):
        return self.hp > 0

    def recibir_daño(self, cantidad):
        self.hp -= cantidad
        if self.hp < 0:
            self.hp = 0

class Base:
    def __init__(self, hp, position):
        self.hp = hp
        self.max_hp = hp
        self.position = position 

    def esta_destruida(self):
        return self.hp <= 0

    def recibir_daño(self, cantidad):
        self.hp -= cantidad
        if self.hp < 0:
            self.hp = 0

TOWERS_CATALOG = {
    "basica": {"name": "Torre básica", "cost": 50, "hp": 100, "damage": 10, "range_": 3, "ability": "double_shot", "cooldown": 3},
    "pesada": {"name": "Torre pesada", "cost": 150, "hp": 250, "damage": 25, "range_": 2, "ability": "area_damage", "cooldown": 4},
    "magica": {"name": "Torre mágica", "cost": 120, "hp": 80, "damage": 5, "range_": 4, "ability": "freeze", "cooldown": 5},
}

UNITS_CATALOG = {
    "soldado": {"name": "Soldado básico", "cost": 40, "hp": 80, "damage": 10, "speed": 1, "ability": "double_attack", "cooldown": 3},
    "tanque": {"name": "Tanque", "cost": 120, "hp": 200, "damage": 15, "speed": 0.5, "ability": "shield", "cooldown": 4},
    "rapida": {"name": "Unidad rápida", "cost": 60, "hp": 50, "damage": 5, "speed": 2, "ability": "speed_boost", "cooldown": 2},
}