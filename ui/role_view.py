import tkinter as tk
from constantes import *

# Pantalla de selección de rol (defensor o atacante)

# Variable global con el rol que el jugador actual va eligiendo en esta pantalla
rol_elegido = None


def mostrar_seleccion_rol(root, img_fondo, numero_jugador=1, rol_tomado=None, on_success=None):
    global rol_elegido
    rol_elegido = None

    # Frame principal
    frame = tk.Frame(root, bg=COLOR_FONDO)
    frame.place(x=0, y=0, width=ANCHO, height=ALTO)

    # Fondo
    canvas = tk.Canvas(frame, width=ANCHO, height=ALTO, highlightthickness=0, bg=COLOR_FONDO)
    canvas.place(x=0, y=0)
    canvas.create_image(0, 0, anchor="nw", image=img_fondo)

    # Título
    canvas.create_text(450, 90, text="CHOOSE YOUR ROLE", font=FUENTE_TITULO, fill=COLOR_1)
    canvas.create_text(450, 130, text="Player " + str(numero_jugador), font=FUENTE_SMALL, fill=COLOR_2)

    # Mensaje de error
    lbl_msg = tk.Label(frame, text="", font=FUENTE_SMALL, bg=COLOR_FONDO, fg=COLOR_ROJO)
    lbl_msg.place(x=450, y=480, anchor="center")

    # Información de las dos tarjetas de rol
    roles_info = [
        ("defensor", "DEFENDER", "Build walls and towers to protect the base", 280),
        ("atacante", "ATTACKER", "Buy units to destroy the enemy base", 620),
    ]

    botones = {}  # guarda el botón de cada rol para poder cambiarle el color

    def seleccionar(rol):
        global rol_elegido
        if rol == rol_tomado:
            return
        rol_elegido = rol
        lbl_msg.config(text="")

        for r in botones:
            btn = botones[r]
            if r == rol:
                btn.config(bg=COLOR_1, fg="#0A1628")
            elif r == rol_tomado:
                btn.config(bg="#444444", fg="#888888")
            else:
                btn.config(bg=COLOR_FONDO, fg=COLOR_2)

    def confirmar():
        if rol_elegido is None:
            lbl_msg.config(text="Please select a role first.")
            return
        if on_success:
            on_success(rol_elegido)

    # Dibujamos las dos tarjetas
    for rol, nombre, descripcion, x in roles_info:
        tomado = (rol == rol_tomado)

        # Fondo de la tarjeta (panel detrás del texto)
        canvas.create_rectangle(x - 160, 200, x + 160, 410, fill=COLOR_PANEL, outline=COLOR_1, width=2)

        if tomado:
            color_texto = "#888888"
        else:
            color_texto = COLOR_2

        canvas.create_text(x, 240, text=nombre, font=FUENTE_BTN, fill=color_texto)
        canvas.create_text(x, 280, text=descripcion, font=FUENTE_SMALL, fill=color_texto, width=260)

        if tomado:
            canvas.create_text(x, 330, text="TAKEN", font=FUENTE_SMALL, fill=COLOR_ROJO)
            color_btn = "#444444"
            color_fg = "#888888"
            cursor_btn = "arrow"
        else:
            color_btn = COLOR_FONDO
            color_fg = COLOR_2
            cursor_btn = "hand2"

        def click_boton_rol(r=rol):
            seleccionar(r)

        btn = tk.Button(frame, text="SELECT", font=FUENTE_BTN, bg=color_btn, fg=color_fg,
                         relief="flat", cursor=cursor_btn, width=14, pady=5,
                         command=click_boton_rol)
        btn.place(x=x, y=370, anchor="center")
        botones[rol] = btn

    # Botón confirmar
    btn_confirmar = tk.Button(frame, text="CONFIRM", font=FUENTE_BTN, bg=COLOR_1, fg="#0A1628",
                               relief="flat", cursor="hand2", width=20, pady=8, command=confirmar)
    btn_confirmar.place(x=450, y=440, anchor="center")
