import tkinter as tk
from constantes import *
from core.data_definitions import TOWERS_CATALOG
from core.economy import COSTO_PARED

# Catálogo de torres y muro.
# hp/daño/rango/cooldown vienen de core/data_definitions.py (el mismo catalogo que usa
# el motor de combate real), asi que lo que se ve en pantalla coincide con lo que pasa
# en el combate. "nombre" e "img" son solo cosas visuales de esta pantalla.
NOMBRES_TIPO = {"basica": "Basic Tower", "pesada": "Heavy Tower", "magica": "Magic Tower", "muro": "Wall"}

TORRES = {}
for _tipo, _datos in TOWERS_CATALOG.items():
    TORRES[_tipo] = {"nombre": NOMBRES_TIPO[_tipo], "costo": _datos["coste"], "hp": _datos["hp"],
                      "daño": _datos["daño"], "rango": _datos["rango"], "img": None}

COSTO_MURO = COSTO_PARED

# Cuantos turnos de cooldown necesita cada torre para activar su habilidad
# (mismo valor que usa el motor de combate real en core/data_definitions.py).
COOLDOWN_MAXIMO = {}
for _tipo, _datos in TOWERS_CATALOG.items():
    COOLDOWN_MAXIMO[_tipo] = _datos["cooldown"]

# Texto corto que describe que hace la habilidad de cada torre
HABILIDAD_TORRE = {
    "basica": "double dmg \n on next hit",
    "pesada": "+20% dm \n for 3 sec",
    "magica": "heals ally \n to full hp",
}

# Variables globales con el estado de la pantalla de defensa
mapa = []
dinero_actual = 0
tipo_seleccionado = None
objetos_colocados = []


def mostrar_mapa_defensor(root, img_fondo, faccion, dinero_inicial, on_turno_listo,
                           faccion_atacante=None,
                           img_messi_arg=None, img_gustavo_arg=None, img_che_arg=None,
                           img_pinguino_madag=None, img_moto_moto_madag=None, img_pinguino_negro_madag=None,
                           img_tech_support_india=None, img_taxi_driver_india=None, img_scammer_india=None):
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


                if contenido == "base":
                    canvas.create_text(cx, cy, text="BASE", font=("Arial", 10, "bold"),
                                        fill=color_de_texto(fill), tags="mapa")
                elif contenido == "muro":
                    canvas.create_text(cx, cy, text="🧱", font=("Segoe UI Emoji", 16),
                                        fill=color_de_texto(fill), tags="mapa")
                elif contenido == "basica":
                    canvas.create_text(cx, cy, text="🏯", font=("Segoe UI Emoji", 16),
                                        fill=color_de_texto(fill), tags="mapa")
                elif contenido == "pesada":
                    canvas.create_text(cx, cy, text="🛡", font=("Segoe UI Emoji", 16),
                                        fill=color_de_texto(fill), tags="mapa")
                elif contenido == "magica":
                    canvas.create_text(cx, cy, text="✨", font=("Segoe UI Emoji", 16),
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

    def borrar_hover(event):
        canvas.delete("hover")

    canvas.bind("<Motion>", hover_celda)
    canvas.bind("<Leave>", borrar_hover)

    # Display de dinero (esquina superior izquierda)
    lbl_dinero = tk.Label(frame, text="$" + str(dinero_actual), font=("Courier New", 14, "bold"),
                           bg="#111111", fg=COLOR_1, padx=10, pady=5)
    lbl_dinero.place(x=10, y=10)

    # Display de facción (igual que en la pantalla del atacante)
    tk.Label(frame, text="Defender - " + faccion, font=("Courier New", 12, "bold"),
              bg="#111111", fg=COLOR_VERDE, padx=10, pady=5).place(x=10, y=50)


        #Preview de los personajes del atacante segun la faccion que eligio
    if faccion_atacante == "Argentina":
        img_enemigo_1 = img_messi_arg
        img_enemigo_2 = img_gustavo_arg
        img_enemigo_3 = img_che_arg
    elif faccion_atacante == "Madagascar":
        img_enemigo_1 = img_pinguino_madag
        img_enemigo_2 = img_moto_moto_madag
        img_enemigo_3 = img_pinguino_negro_madag
    elif faccion_atacante == "India":
        img_enemigo_1 = img_tech_support_india
        img_enemigo_2 = img_taxi_driver_india
        img_enemigo_3 = img_scammer_india
    else:
        img_enemigo_1 = None
        img_enemigo_2 = None
        img_enemigo_3 = None

    tk.Label(frame, text="Enemy troops:", font=("Courier New", 9, "bold"),
              bg="#111111", fg=COLOR_2, padx=8, pady=4).place(x=ANCHO_MAPA - 10, y=55, anchor="ne")


    x_columna_enemigos = ANCHO_MAPA - 45
    if img_enemigo_1:
        canvas.create_image(x_columna_enemigos, 110, image=img_enemigo_1, tags="preview")
    if img_enemigo_2:
        canvas.create_image(x_columna_enemigos, 170, image=img_enemigo_2, tags="preview")
    if img_enemigo_3:
        canvas.create_image(x_columna_enemigos, 230, image=img_enemigo_3, tags="preview")

    # Panel con la informacion de la habilidad de cada tipo de torre
    # (debajo de la vista previa del atacante, en el mismo margen de la derecha)
    texto_habilidades = ("ABILITIES\n\n"
                          "Basic:\n" + HABILIDAD_TORRE["basica"] + "\n\n"
                          "Heavy:\n" + HABILIDAD_TORRE["pesada"] + "\n\n"
                          "Magic:\n" + HABILIDAD_TORRE["magica"])
    tk.Label(frame, text=texto_habilidades, font=("Courier New", 7, "bold"),
              bg="#111111", fg=COLOR_2, justify="left", padx=3, pady=4).place(x=ANCHO_MAPA - 10, y=280, anchor="ne")

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

        def click_boton_item(t=tipo, b=btn):
            seleccionar_item(t, b)

        btn.config(command=click_boton_item)

    # Botón limpiar celda
    def click_boton_limpiar():
        seleccionar_item("limpiar", btn_limpiar)

    btn_limpiar = tk.Button(frame, text="Clear", font=FUENTE_SMALL, bg=COLOR_ROJO, fg="#FFFFFF",
                             relief="flat", cursor="hand2", width=9, pady=3,
                             command=click_boton_limpiar)
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
        on_turno_listo(objetos_colocados, dinero_actual)

    tk.Button(frame, text="End Turn", font=FUENTE_BTN, bg=COLOR_VERDE, fg="#0A1628",
              relief="flat", cursor="hand2", padx=15, pady=5,
              command=terminar_turno).place(x=ANCHO_MAPA - 10, y=10, anchor="ne")

    dibujar_mapa()
