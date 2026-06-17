class Tower:
    def __init__(self, nombre, coste, hp, daño, rango, habilidad, cooldown):
        self.nombre = nombre
        self.coste = coste
        self.hp = hp
        self.max_hp = hp
        self.daño = daño
        self.rango = rango
        self.habilidad = habilidad
        self.cooldown = cooldown  #turnos para activar habilidad
        self.cooldown_actual = 0
        self.position = None  #va a ser (fila, columna)
 
    def esta_vivo(self):
        return self.hp > 0
 
    def recibir_daño(self, cantidad):
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
 
 
class Unidad:
    def __init__(self, nombre, coste, hp, daño, velocidad, habilidad, cooldown):
        self.nombre = nombre
        self.coste = coste
        self.hp = hp
        self.max_hp = hp
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
    def __init__(self, coste, hp):
        self.coste = coste
        self.hp = hp
        self.max_hp = hp
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