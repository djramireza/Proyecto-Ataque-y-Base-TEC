import tkinter as tk
from constantes import *

# Pantalla de selección de facción

# Variable global con la facción que el jugador actual va eligiendo en esta pantalla
faccion_elegida = None


def mostrar_facciones(root, img_fondo, img_madagascar, img_argentina, img_india,
                       numero_jugador=1, faccion_tomada=None, on_success=None):
    global faccion_elegida
    faccion_elegida = None

    # Frame principal
    frame = tk.Frame(root, bg=COLOR_FONDO)
    frame.place(x=0, y=0, width=ANCHO, height=ALTO)

    # Fondo
    canvas = tk.Canvas(frame, width=ANCHO, height=ALTO, highlightthickness=0, bg=COLOR_FONDO)
    canvas.place(x=0, y=0)
    canvas.create_image(0, 0, anchor="nw", image=img_fondo)

    # Título
    canvas.create_text(450, 90, text="CHOOSE YOUR FACTION", font=FUENTE_TITULO, fill=COLOR_1)
    canvas.create_text(450, 130, text="Player " + str(numero_jugador), font=FUENTE_SMALL, fill=COLOR_2)

    # Mensaje de error
    lbl_msg = tk.Label(frame, text="", font=FUENTE_SMALL, bg=COLOR_FONDO, fg=COLOR_ROJO)
    lbl_msg.place(x=450, y=530, anchor="center")

    # Tarjetas de facciones
    facciones_info = [
        ("Madagascar", img_madagascar, 175),
        ("Argentina", img_argentina, 450),
        ("India", img_india, 725),
    ]

    botones = {}  # guarda el botón de cada facción para poder cambiarle el color

    def seleccionar(nombre):
        global faccion_elegida
        if nombre == faccion_tomada:
            return
        faccion_elegida = nombre
        lbl_msg.config(text="")

        for n in botones:
            btn = botones[n]
            if n == nombre:
                btn.config(bg=COLOR_1, fg="#0A1628")
            elif n == faccion_tomada:
                btn.config(bg="#444444", fg="#888888")
            else:
                btn.config(bg=COLOR_FONDO, fg=COLOR_2)

    def confirmar():
        if faccion_elegida is None:
            lbl_msg.config(text="Please select a faction first.")
            return
        if on_success:
            on_success(faccion_elegida)

    # Dibujamos las tres tarjetas
    for nombre, imagen, x in facciones_info:
        tomada = (nombre == faccion_tomada)

        canvas.create_image(x, 280, anchor="center", image=imagen)

        if tomada:
            color_texto = "#888888"
        else:
            color_texto = COLOR_2

        canvas.create_text(x, 385, text=nombre, font=FUENTE_BTN, fill=color_texto)

        if tomada:
            canvas.create_text(x, 410, text="TAKEN", font=FUENTE_SMALL, fill=COLOR_ROJO)
            color_btn = "#444444"
            color_fg = "#888888"
            cursor_btn = "arrow"
        else:
            color_btn = COLOR_FONDO
            color_fg = COLOR_2
            cursor_btn = "hand2"

        def click_boton_faccion(n=nombre):
            seleccionar(n)

        btn = tk.Button(frame, text="SELECT", font=FUENTE_BTN, bg=color_btn, fg=color_fg,
                         relief="flat", cursor=cursor_btn, width=12, pady=5,
                         command=click_boton_faccion)
        btn.place(x=x, y=430, anchor="center")
        botones[nombre] = btn

    # Botón confirmar
    btn_confirmar = tk.Button(frame, text="CONFIRM", font=FUENTE_BTN, bg=COLOR_1, fg="#0A1628",
                               relief="flat", cursor="hand2", width=20, pady=8, command=confirmar)
    btn_confirmar.place(x=450, y=490, anchor="center")
