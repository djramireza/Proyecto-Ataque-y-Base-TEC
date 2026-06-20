import json
import os 

PLAYERS_FILE = "data/players.json"
 
def cargar_jugadores():#lee el archivo JSON y devuelve un diccionario con todos los jugadores
    if not os.path.exists(PLAYERS_FILE):
        return {}
    with open(PLAYERS_FILE, "r") as f:
        return json.load(f)
 
 
def guardar_jugadores(jugadores):#sobrescribe el archivo JSON con el diccionario actualizado
    os.makedirs(os.path.dirname(PLAYERS_FILE), exist_ok=True)
    with open(PLAYERS_FILE, "w") as f:
        json.dump(jugadores, f, indent=4)
 
 
def obtener_jugador(username):#devuelve los datos de un jugador o None si no existe
    jugadores = cargar_jugadores()
    return jugadores.get(username, None)
 
 
def actualizar_victoria(username, rol):#rol debe ser "defensor" o "atacante"
    jugadores = cargar_jugadores()
    if username not in jugadores:
        return False, "Jugador no encontrado"
    if rol == "defensor":
        jugadores[username]["wins_defensor"] += 1
    elif rol == "atacante":
        jugadores[username]["wins_atacante"] += 1
    else:
        return False, "Rol inválido"
    guardar_jugadores(jugadores)
    return True, "Victoria registrada"
 
 
def obtener_top_jugadores(rol, limite=5):#devuelve los top jugadores ordenados por victorias segun el rol
                                         #rol debe ser "defensor" o "atacante"
    jugadores = cargar_jugadores()
    clave = f"wins_{rol}"
 
    ranking = [
        {"username": username, "victorias": datos[clave]} for username, datos in jugadores.items()]
    ranking.sort(key=lambda x: x["victorias"], reverse=True)
    return ranking[:limite]