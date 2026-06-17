from data_manager import cargar_jugadores, guardar_jugadores
import json
import os

PLAYERS_FILE = "data/players.json"

def registrar_jugador(username, password):#crea un nuevo jugador, devuelve (True, mensaje) o (False, mensaje)
    if not username or not password:
        return False, "Usuario y contraseña no pueden estar vacíos"
 
    jugadores = cargar_jugadores()
    if username in jugadores:
        return False, "El usuario ya existe"
 
    jugadores[username] = {"password": password, "wins_defensor": 0, "wins_atacante": 0}
    guardar_jugadores(jugadores)
    return True, "Jugador registrado correctamente"

def iniciar_sesion(username, password):#verifica usuario y contraseña, devuelve (True, mensaje) o (False, mensaje)
    if not username or not password:
        return False, "Usuario y contraseña no pueden estar vacíos"
 
    jugadores = cargar_jugadores()
    if username not in jugadores:
        return False, "Usuario no encontrado"
    if jugadores[username]["password"] != password:
        return False, "Contraseña incorrecta"
    return True, "Inicio de sesión exitoso"