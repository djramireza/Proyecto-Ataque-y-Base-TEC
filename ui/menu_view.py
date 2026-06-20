import tkinter as tk
from constantes import *

# Pantalla del menu principal


def mostrar_menu_principal(root, img_fondo, on_comenzar=None, on_ver_leaderboard=None, on_salir=None):
    frame = tk.Frame(root, bg=COLOR_FONDO)
    frame.place(x=0, y=0, width=ANCHO, height=ALTO)

    canvas = tk.Canvas(frame, width=ANCHO, height=ALTO, highlightthickness=0, bg=COLOR_FONDO)
    canvas.place(x=0, y=0)
    canvas.create_image(0, 0, anchor="nw", image=img_fondo)

    canvas.create_text(450, 150, text="TOWER DEFENSE", font=FUENTE_TITULO, fill=COLOR_1)
    canvas.create_text(450, 200, text="Base Defense and Assault", font=FUENTE_SMALL, fill=COLOR_2)

    def comenzar():
        if on_comenzar:
            on_comenzar()

    def ver_leaderboard():
        if on_ver_leaderboard:
            on_ver_leaderboard()

    def salir():
        if on_salir:
            on_salir()
        else:
            root.destroy()

    btn_comenzar = tk.Button(frame, text="START", font=FUENTE_BTN, bg=COLOR_1, fg="#0A1628",
                              relief="flat", cursor="hand2", width=22, pady=8, command=comenzar)
    btn_comenzar.place(x=450, y=350, anchor="center")

    btn_leaderboard = tk.Button(frame, text="LEADERBOARD", font=FUENTE_BTN, bg=COLOR_FONDO, fg=COLOR_2,
                                 relief="flat", cursor="hand2", width=22, pady=8, command=ver_leaderboard)
    btn_leaderboard.place(x=450, y=410, anchor="center")

    btn_salir = tk.Button(frame, text="EXIT", font=FUENTE_BTN, bg=COLOR_FONDO, fg=COLOR_2,
                           relief="flat", cursor="hand2", width=22, pady=8, command=salir)
    btn_salir.place(x=450, y=470, anchor="center")
