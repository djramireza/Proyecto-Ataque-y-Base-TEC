import tkinter as tk
from constantes import *
from core.data_manager import obtener_top_jugadores

# Pantalla del leaderboard, muestra los 5 con mas victorias como defensor
# y los 5 con mas victorias como atacante


def obtener_leaderboard():
    defensores = obtener_top_jugadores("defensor")
    atacantes = obtener_top_jugadores("atacante")
    return {"defensores": defensores, "atacantes": atacantes}


def mostrar_leaderboard(root, img_fondo, on_volver=None):
    frame = tk.Frame(root, bg=COLOR_FONDO)
    frame.place(x=0, y=0, width=ANCHO, height=ALTO)

    canvas = tk.Canvas(frame, width=ANCHO, height=ALTO, highlightthickness=0, bg=COLOR_FONDO)
    canvas.place(x=0, y=0)
    canvas.create_image(0, 0, anchor="nw", image=img_fondo)

    canvas.create_text(450, 80, text="LEADERBOARD", font=FUENTE_TITULO, fill=COLOR_1)

    datos = obtener_leaderboard()

    def dibujar_tabla(titulo, lista, x):
        panel = tk.Frame(frame, bg=COLOR_PANEL, padx=24, pady=20,
                          highlightbackground=COLOR_1, highlightthickness=1)
        canvas.create_window(x, 330, window=panel)

        tk.Label(panel, text=titulo, font=("Courier New", 13, "bold"),
                 bg=COLOR_PANEL, fg=COLOR_1).grid(row=0, column=0, columnspan=2, pady=(0, 14))

        if not lista:
            tk.Label(panel, text="No data yet", font=FUENTE_SMALL,
                     bg=COLOR_PANEL, fg=COLOR_2).grid(row=1, column=0, columnspan=2)
            return

        fila = 1
        puesto = 1
        for jugador in lista[:5]:
            nombre = jugador["username"]
            victorias = jugador["victorias"]
            tk.Label(panel, text=str(puesto) + ". " + nombre, font=FUENTE_SMALL,
                     bg=COLOR_PANEL, fg=COLOR_2, width=16, anchor="w").grid(row=fila, column=0, sticky="w", pady=2)
            tk.Label(panel, text=str(victorias) + " wins", font=FUENTE_SMALL,
                     bg=COLOR_PANEL, fg=COLOR_VERDE, width=8, anchor="e").grid(row=fila, column=1, sticky="e", pady=2)
            fila = fila + 1
            puesto = puesto + 1

    dibujar_tabla("TOP DEFENDERS", datos["defensores"], 280)
    dibujar_tabla("TOP ATTACKERS", datos["atacantes"], 620)

    def volver():
        if on_volver:
            on_volver()

    btn_volver = tk.Button(frame, text="BACK TO MENU", font=FUENTE_BTN, bg=COLOR_1, fg="#0A1628",
                            relief="flat", cursor="hand2", width=20, pady=8, command=volver)
    btn_volver.place(x=450, y=530, anchor="center")
