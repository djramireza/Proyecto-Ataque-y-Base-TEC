
# Tamaño de la ventana (pantallas de login, rol y facción)
ANCHO = 900
ALTO = 600

# Colores y fuentes
COLOR_FONDO = "#0A1628"
COLOR_PANEL = "#858585"
COLOR_1 = "#fffc39"
COLOR_1_HOV = "#D6C44C"
COLOR_TEXTO = "#F0E6D3"
COLOR_2 = "#FFFFFF"
COLOR_ROJO = "#860019"
COLOR_VERDE = "#4DFFB4"

FUENTE_TITULO = ("Georgia", 45, "bold")
FUENTE_LABEL = ("Courier New", 10, "bold")
FUENTE_ENTRY = ("Courier New", 11)
FUENTE_BTN = ("Courier New", 11, "bold")
FUENTE_SMALL = ("Courier New", 10)

# Facciones disponibles
FACCIONES = ["Madagascar", "Argentina", "India"]

# Tamaño de la ventana del mapa (defensa, ataque y combate)
ANCHO_MAPA = 1080
ALTO_MAPA = 720

# Configuración del mapa (cuadrícula)
FILAS = 9
COLUMNAS = 16
CELDA = 54

# La cuadrícula se dibuja un poco corrida para quedar centrada
GRID_X = 106
GRID_Y = 120

# La base va del lado derecho, en el medio
BASE_FILA = 4
BASE_COL = 14

# Vida de la base y de cada muro (se usa en la pantalla de combate)
BASE_HP = 300
MURO_HP = 40

COLOR_BORDE = "#445566"
COLOR_BASE = "#FF4D6D"
COLOR_TORRE = "#C8A951"
COLOR_MURO = "#888888"
COLOR_UNIDAD = "#4DFFB4"

# Colores de la base, el muro y las torres según la facción elegida
# (basados en los colores de la bandera de cada país)
FACCION_COLORES = {
    "Madagascar": {
        "base": "#CE1126",
        "muro": "#FFFFFF",
        "torre_basica": "#007E3A",
        "torre_pesada": "#CE1126",
        "torre_magica": "#FFFFFF",
    },
    "Argentina": {
        "base": "#75AADB",
        "muro": "#FFFFFF",
        "torre_basica": "#75AADB",
        "torre_pesada": "#4A7FB5",
        "torre_magica": "#F6B40E",
    },
    "India": {
        "base": "#FF9933",
        "muro": "#FFFFFF",
        "torre_basica": "#138808",
        "torre_pesada": "#FF9933",
        "torre_magica": "#000080",
    },
}


def color_de_texto(color_fondo):
    # Si el fondo es un color claro usamos texto negro, si es oscuro usamos blanco.
    # Lista simple de los colores claros que usamos en el juego.
    colores_claros = ["#FFFFFF", "#F6B40E", "#FF9933", "#fffc39"]
    if color_fondo in colores_claros:
        return "#0A1628"
    else:
        return "#FFFFFF"
