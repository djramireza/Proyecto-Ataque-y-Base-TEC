import tkinter as tk
from constantes import *

# Catálogo de torres y muro
# Cuando Romu conecte el core, estos datos se reemplazan por los del core/economy.py
TORRES = {
    "basica": {"nombre": "Basic Tower", "costo": 50, "hp": 100, "daño": 10, "rango": 3, "img": None},
    "pesada": {"nombre": "Heavy Tower", "costo": 150, "hp": 250, "daño": 25, "rango": 2, "img": None},
    "magica": {"nombre": "Magic Tower", "costo": 120, "hp": 80, "daño": 5, "rango": 4, "img": None},
}
COSTO_MURO = 10

NOMBRES_TIPO = {"basica": "Basic Tower", "pesada": "Heavy Tower", "magica": "Magic Tower", "muro": "Wall"}

# Variables globales con el estado de la pantalla de defensa
mapa = []
dinero_actual = 0
tipo_seleccionado = None
objetos_colocados = []


def mostrar_mapa_defensor(root, img_fondo, img_base, faccion, dinero_inicial, on_turno_listo):
    global mapa, dinero_actual, tipo_seleccionado, objetos_colocados

    root.geometry(str(ANCHO_MAPA) + "x" + str(ALTO_MAPA))

    colores = FACCION_COLORES.get(faccion, FACCION_COLORES[FACCIONES[0]])

    # Reiniciamos el estado cada vez que se muestra esta pantalla
    mapa = []
    for f in range(FILAS):
        fila = []
        for c in range(COLUMNAS):
            fila.append(None)
        mapa.append(fila)
    mapa[BASE_FILA][BASE_COL] = "base"

    dinero_actual = dinero_inicial
    tipo_seleccionado = None
    objetos_colocados = []

    # Interfaz
    frame = tk.Frame(root, bg=COLOR_FONDO)
    frame.place(x=0, y=0, width=ANCHO_MAPA, height=ALTO_MAPA)

    canvas = tk.Canvas(frame, width=ANCHO_MAPA, height=ALTO_MAPA, highlightthickness=0, bg=COLOR_FONDO)
    canvas.place(x=0, y=0)
    canvas.create_image(0, 0, anchor="nw", image=img_fondo)

    def dibujar_mapa():
        canvas.delete("mapa")
        for f in range(FILAS):
            for c in range(COLUMNAS):
                x1 = GRID_X + c * CELDA
                y1 = GRID_Y + f * CELDA
                x2 = x1 + CELDA
                y2 = y1 + CELDA
                cx = x1 + CELDA // 2
                cy = y1 + CELDA // 2

                contenido = mapa[f][c]

                if contenido == "base":
                    fill = colores["base"]
                elif contenido == "basica" or contenido == "pesada" or contenido == "magica":
                    fill = colores["torre_" + contenido]
                elif contenido == "muro":
                    fill = colores["muro"]
                else:
                    fill = ""

                canvas.create_rectangle(x1, y1, x2, y2, fill=fill, outline="#FFFFFF", width=1, tags="mapa")

                if contenido == "base" and img_base:
                    canvas.create_image(cx, cy, image=img_base, tags="mapa")
                elif contenido == "base":
                    canvas.create_text(cx, cy, text="BASE", font=("Arial", 10, "bold"),
                                        fill=color_de_texto(fill), tags="mapa")
                elif contenido == "muro":
                    canvas.create_text(cx, cy, text="WALL", font=("Arial", 9, "bold"),
                                        fill=color_de_texto(fill), tags="mapa")
                elif contenido == "basica":
                    canvas.create_text(cx, cy, text="BAS", font=("Arial", 10, "bold"),
                                        fill=color_de_texto(fill), tags="mapa")
                elif contenido == "pesada":
                    canvas.create_text(cx, cy, text="PES", font=("Arial", 10, "bold"),
                                        fill=color_de_texto(fill), tags="mapa")
                elif contenido == "magica":
                    canvas.create_text(cx, cy, text="MAG", font=("Arial", 10, "bold"),
                                        fill=color_de_texto(fill), tags="mapa")

    def click_celda(event):
        global dinero_actual

        c = (event.x - GRID_X) // CELDA
        f = (event.y - GRID_Y) // CELDA
        if not (0 <= f < FILAS and 0 <= c < COLUMNAS):
            return
        if mapa[f][c] == "base":
            lbl_msg.config(text="You can't build on the base.", fg=COLOR_ROJO)
            return

        tipo = tipo_seleccionado
        if tipo is None:
            lbl_msg.config(text="Select a tower or wall first.", fg=COLOR_ROJO)
            return

        if mapa[f][c] is not None:
            lbl_msg.config(text="Cell occupied. Use Clear first.", fg=COLOR_ROJO)
            return

        if tipo == "muro":
            costo = COSTO_MURO
        else:
            costo = TORRES[tipo]["costo"]

        if dinero_actual < costo:
            lbl_msg.config(text="Not enough money. (You need $" + str(costo) + ")", fg=COLOR_ROJO)
            return

        mapa[f][c] = tipo
        dinero_actual = dinero_actual - costo
        objetos_colocados.append({"tipo": tipo, "posicion": (f, c)})
        lbl_dinero.config(text="$" + str(dinero_actual))
        lbl_msg.config(text=NOMBRES_TIPO[tipo] + " placed at (" + str(f) + "," + str(c) + ")  -  Cost: $" + str(costo),
                        fg=COLOR_VERDE)
        dibujar_mapa()

    def hover_celda(event):
        c = (event.x - GRID_X) // CELDA
        f = (event.y - GRID_Y) // CELDA
        canvas.delete("hover")
        if 0 <= f < FILAS and 0 <= c < COLUMNAS and mapa[f][c] != "base":
            x1 = GRID_X + c * CELDA
            y1 = GRID_Y + f * CELDA
            canvas.create_rectangle(x1, y1, x1 + CELDA, y1 + CELDA, outline=COLOR_1, width=2, tags="hover")

    canvas.bind("<Motion>", hover_celda)
    canvas.bind("<Leave>", lambda e: canvas.delete("hover"))

    # Display de dinero (esquina superior izquierda)
    lbl_dinero = tk.Label(frame, text="$" + str(dinero_actual), font=("Courier New", 14, "bold"),
                           bg="#111111", fg=COLOR_1, padx=10, pady=5)
    lbl_dinero.place(x=10, y=10)

    # Panel de compra (gradas de abajo)
    Y_PANEL = GRID_Y + FILAS * CELDA + 8

    items = [
        ("Basic\n$" + str(TORRES["basica"]["costo"]), "basica", colores["torre_basica"], color_de_texto(colores["torre_basica"])),
        ("Heavy\n$" + str(TORRES["pesada"]["costo"]), "pesada", colores["torre_pesada"], color_de_texto(colores["torre_pesada"])),
        ("Magic\n$" + str(TORRES["magica"]["costo"]), "magica", colores["torre_magica"], color_de_texto(colores["torre_magica"])),
        ("Wall\n$" + str(COSTO_MURO), "muro", colores["muro"], color_de_texto(colores["muro"])),
    ]

    total_ancho = len(items) * 110 + (len(items) - 1) * 10
    x_inicio = (ANCHO_MAPA - total_ancho) // 2
    botones_ref = {}

    def seleccionar_item(tipo, btn_ref):
        global tipo_seleccionado
        tipo_seleccionado = tipo
        if tipo == "limpiar":
            nombre = "Clear"
        else:
            nombre = NOMBRES_TIPO[tipo]
        lbl_msg.config(text="Selected: " + nombre + " - Click a cell to place it")
        for t in botones_ref:
            botones_ref[t].config(relief="flat")
        btn_ref.config(relief="sunken")

    for i in range(len(items)):
        texto, tipo, bg, fg = items[i]
        x = x_inicio + i * 120
        btn = tk.Button(frame, text=texto, font=FUENTE_SMALL, bg=bg, fg=fg, relief="flat",
                         cursor="hand2", width=9, pady=3)
        btn.place(x=x, y=Y_PANEL)
        botones_ref[tipo] = btn
        btn.config(command=lambda t=tipo, b=btn: seleccionar_item(t, b))

    # Botón limpiar celda
    btn_limpiar = tk.Button(frame, text="Clear", font=FUENTE_SMALL, bg=COLOR_ROJO, fg="#FFFFFF",
                             relief="flat", cursor="hand2", width=9, pady=3,
                             command=lambda: seleccionar_item("limpiar", btn_limpiar))
    btn_limpiar.place(x=x_inicio + len(items) * 120, y=Y_PANEL)
    botones_ref["limpiar"] = btn_limpiar

    def click_limpiar(event):
        global dinero_actual

        if tipo_seleccionado != "limpiar":
            return
        c = (event.x - GRID_X) // CELDA
        f = (event.y - GRID_Y) // CELDA
        if not (0 <= f < FILAS and 0 <= c < COLUMNAS):
            return
        if mapa[f][c] is None or mapa[f][c] == "base":
            return

        tipo_anterior = mapa[f][c]
        if tipo_anterior == "muro":
            costo = COSTO_MURO
        else:
            costo = TORRES[tipo_anterior]["costo"]

        dinero_actual = dinero_actual + costo
        lbl_dinero.config(text="$" + str(dinero_actual))
        mapa[f][c] = None

        nueva_lista = []
        for o in objetos_colocados:
            if o["posicion"] != (f, c):
                nueva_lista.append(o)
        objetos_colocados[:] = nueva_lista

        lbl_msg.config(text="Cell cleared - $" + str(costo) + " refunded", fg=COLOR_VERDE)
        dibujar_mapa()

    def click_canvas(event):
        if tipo_seleccionado == "limpiar":
            click_limpiar(event)
        else:
            click_celda(event)

    canvas.bind("<Button-1>", click_canvas)

    # Mensaje de feedback
    lbl_msg = tk.Label(frame, text="Select what you want to build", font=FUENTE_SMALL,
                        bg=COLOR_FONDO, fg=COLOR_2)
    lbl_msg.place(x=ANCHO_MAPA // 2, y=Y_PANEL + 55, anchor="n")

    # Botón terminar turno
    def terminar_turno():
        on_turno_listo(objetos_colocados)

    tk.Button(frame, text="End Turn", font=FUENTE_BTN, bg=COLOR_VERDE, fg="#0A1628",
              relief="flat", cursor="hand2", padx=15, pady=5,
              command=terminar_turno).place(x=ANCHO_MAPA - 10, y=10, anchor="ne")

    dibujar_mapa()


# Prueba rápida de esta pantalla sola
if __name__ == "__main__":
    from PIL import Image, ImageTk
    import os
    folder = os.path.dirname(__file__)

    root = tk.Tk()
    root.title("Defender Turn")
    root.resizable(False, False)

    img_fondo = ImageTk.PhotoImage(
        Image.open(os.path.join(folder, "game_bg.png")).resize((ANCHO_MAPA, ALTO_MAPA), Image.LANCZOS)
    )
    img_base = None

    def turno_listo(objetos):
        print("Defender finished:", objetos)

    mostrar_mapa_defensor(root, img_fondo=img_fondo, img_base=img_base,
                           faccion="Argentina", dinero_inicial=200, on_turno_listo=turno_listo)
    root.mainloop()
