import json
import os

PLAYERS_FILE = "data/players.json"

def crear_jugador(): #lee el archivo json y devuelve un diccionario con todos los jugadores
    if not os.path.exists(PLAYERS_FILE):
        return {}
    with open(PLAYERS_FILE, "r") as f:
        return json.load(f)
    
def guardar_jugadores(jugadores): #sobreescribe el archivo json con el diccionario actualizado
    with open(PLAYERS_FILE, "w") as f:
        json.dump(jugadores, f, indent=4)

def registrar_jugadores(username, password): #va a buscar el username en el json y de ahi responde si existe ya el usuario o no
    jugadores = crear_jugador()
    if username in jugadores:
        return "El usuario ya existe"
    jugadores[username] = {"password": password, "victorias_defensa": 0, "victorias_ataque": 0}
    guardar_jugadores(jugadores)
    return "El usuario fue registrado"

def iniciar_sesion(username, password): #aqui se va a buscar cada usuario y contraseña en el json
    jugadores = crear_jugador()
    if username not in jugadores:
        return "Usuario no encontrado"
    if jugadores[username] ["password"] != password:
        return "Contraseña incorrecta"
    return "Inicio de sesion exitoso"

def actualizar_usuario(username, rol): #aqui debe recibir el nombre de la persona y un roll que es defensor o atacante
    jugadores = crear_jugador()
    if username not in jugadores:
        return False
    if rol == "defensor":
        jugadores[username]["victorias_defensa"] += 1
    elif rol == "atacante":
        jugadores[username]["victorias_atacante"] += 1
    else:
        return False
    guardar_jugadores(jugadores)
    return True

