import tkinter as tk
from constantes import *

# Pantalla de selección y compra de unidades del atacante

# Catálogo de unidades por facción.
# Cada unidad tiene: nombre, costo, hp (vida), daño y velocidad.
# Las unidades estan agrupadas en 3 tipos segun sus estadisticas:
# Regular: vida normal, daño normal, velocidad normal
# Rapida: menos vida, menos daño, pero muy rapida
# Pesada: mas vida, mas daño, pero mas lenta
UNIDADES_POR_FACCION = {
    "Madagascar": {
        "pinguino": {"nombre": "Penguin", "tipo_tropa": "regular", "costo": 70, "hp": 100, "daño": 15, "velocidad": 1},
        "moto_moto": {"nombre": "Moto Moto", "tipo_tropa": "pesada", "costo": 110, "hp": 180, "daño": 25, "velocidad": 0.5},
        "pinguino_negro": {"nombre": "Black Penguin", "tipo_tropa": "rapida", "costo": 50, "hp": 60, "daño": 8, "velocidad": 2.5},
    },
    "Argentina": {
        "messi": {"nombre": "Messi", "tipo_tropa": "rapida", "costo": 50, "hp": 60, "daño": 8, "velocidad": 2.5},
        "cerati": {"nombre": "Gustavo Cerati", "tipo_tropa": "regular", "costo": 70, "hp": 100, "daño": 15, "velocidad": 1},
        "che": {"nombre": "El Che", "tipo_tropa": "pesada", "costo": 110, "hp": 180, "daño": 25, "velocidad": 0.5},
    },
    "India": {
        "tech_support": {"nombre": "Tech Support", "tipo_tropa": "pesada", "costo": 110, "hp": 180, "daño": 25, "velocidad": 0.5},
        "taxi_driver": {"nombre": "Taxi Driver", "tipo_tropa": "rapida", "costo": 50, "hp": 60, "daño": 8, "velocidad": 2.5},
        "scammer": {"nombre": "Scammer", "tipo_tropa": "regular", "costo": 70, "hp": 100, "daño": 15, "velocidad": 1},
    },
}

# Etiquetas de texto placeholder por unidad (se usan cuando no hay imagen)
ETIQUETAS = {
    "pinguino": "PNG", "moto_moto": "MOTO", "pinguino_negro": "PNG2",
    "messi": "MESSI", "cerati": "CER", "che": "CHE",
    "tech_support": "TECH", "taxi_driver": "TAXI", "scammer": "SCAM",
}

# Variables globales con el estado de la pantalla de ataque
mapa_atacante = []
dinero_actual_atacante = 0
tipo_seleccionado_atacante = None
unidades_colocadas = []


def mostrar_mapa_atacante(root, img_fondo, faccion, faccion_defensor, dinero_inicial, on_turno_listo,
                           img_messi_arg=None, img_gustavo_arg=None, img_che_arg=None,
                           img_pinguino_madag=None, img_moto_moto_madag=None, img_pinguino_negro_madag=None,
                           img_tech_support_india=None, img_taxi_driver_india=None, img_scammer_india=None):
    global mapa_atacante, dinero_actual_atacante, tipo_seleccionado_atacante, unidades_colocadas

    root.geometry(str(ANCHO_MAPA) + "x" + str(ALTO_MAPA))

    unidades_faccion = UNIDADES_POR_FACCION[faccion]
    colores_defensor = FACCION_COLORES.get(faccion_defensor, FACCION_COLORES[FACCIONES[0]])

    # Reiniciamos el estado cada vez que se muestra esta pantalla
    mapa_atacante = []
    for f in range(FILAS):
        fila = []
        for c in range(COLUMNAS):
            fila.append(None)
        mapa_atacante.append(fila)
    mapa_atacante[BASE_FILA][BASE_COL] = "base"

    dinero_actual_atacante = dinero_inicial
    tipo_seleccionado_atacante = None
    unidades_colocadas = []

    # Interfaz
    frame = tk.Frame(root, bg=COLOR_FONDO)
    frame.place(x=0, y=0, width=ANCHO_MAPA, height=ALTO_MAPA)

    canvas = tk.Canvas(frame, width=ANCHO_MAPA, height=ALTO_MAPA, highlightthickness=0, bg=COLOR_FONDO)
    canvas.place(x=0, y=0)
    canvas.create_image(0, 0, anchor="nw", image=img_fondo)

    # Esta funcion devuelve la imagen que le toca a cada tipo de unidad.
    # Si el tipo no tiene imagen todavia, devuelve None.
    def imagen_de_unidad(tipo):
        if tipo == "messi":
            return img_messi_arg
        elif tipo == "cerati":
            return img_gustavo_arg
        elif tipo == "che":
            return img_che_arg
        elif tipo == "pinguino":
            return img_pinguino_madag
        elif tipo == "moto_moto":
            return img_moto_moto_madag
        elif tipo == "pinguino_negro":
            return img_pinguino_negro_madag
        elif tipo == "tech_support":
            return img_tech_support_india
        elif tipo == "taxi_driver":
            return img_taxi_driver_india
        elif tipo == "scammer":
            return img_scammer_india
        else:
            return None

    # Dibuja todas las casillas del mapa con lo que haya en cada una
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

                contenido = mapa_atacante[f][c]

                if contenido == "base":
                    fill = colores_defensor["base"]
                elif contenido in unidades_faccion:
                    fill = COLOR_UNIDAD
                else:
                    fill = ""

                canvas.create_rectangle(x1, y1, x2, y2, fill=fill, outline="#FFFFFF", width=1, tags="mapa")

                imagen_unidad = imagen_de_unidad(contenido)

                if contenido == "base":
                    canvas.create_text(cx, cy, text="BASE", font=("Arial", 10, "bold"),
                                        fill=color_de_texto(fill), tags="mapa")
                elif imagen_unidad:
                    canvas.create_image(cx, cy, image=imagen_unidad, tags="mapa")
                elif contenido in unidades_faccion:
                    etiqueta = ETIQUETAS.get(contenido, "UNI")
                    canvas.create_text(cx, cy, text=etiqueta, font=("Arial", 9, "bold"), tags="mapa")
                elif c == 0:
                    canvas.create_text(cx, cy, text="IN", font=("Arial", 11, "bold"), fill=COLOR_VERDE, tags="mapa")

    # Cuando el jugador hace click en una casilla del mapa
    def click_celda(event):
        global dinero_actual_atacante

        c = (event.x - GRID_X) // CELDA
        f = (event.y - GRID_Y) // CELDA
        if not (0 <= f < FILAS and 0 <= c < COLUMNAS):
            return
        if mapa_atacante[f][c] == "base":
            lbl_msg.config(text="You can't step on the base.", fg=COLOR_ROJO)
            return
        if c != 0:
            lbl_msg.config(text="Units can only enter through the left column (IN).", fg=COLOR_ROJO)
            return

        tipo = tipo_seleccionado_atacante
        if tipo is None:
            lbl_msg.config(text="Select a unit first.", fg=COLOR_ROJO)
            return

        if tipo == "limpiar":
            if mapa_atacante[f][c] is not None and mapa_atacante[f][c] != "base":
                costo = unidades_faccion[mapa_atacante[f][c]]["costo"]
                dinero_actual_atacante = dinero_actual_atacante + costo
                lbl_dinero.config(text="$" + str(dinero_actual_atacante))

                nueva_lista = []
                for u in unidades_colocadas:
                    if u["posicion"] != (f, c):
                        nueva_lista.append(u)
                unidades_colocadas[:] = nueva_lista

                mapa_atacante[f][c] = None
                lbl_msg.config(text="Unit removed - $" + str(costo) + " refunded", fg=COLOR_VERDE)
                dibujar_mapa()
            return

        if mapa_atacante[f][c] is not None:
            lbl_msg.config(text="Cell occupied. Use Clear first.", fg=COLOR_ROJO)
            return

        costo = unidades_faccion[tipo]["costo"]
        if dinero_actual_atacante < costo:
            lbl_msg.config(text="Not enough money. (You need $" + str(costo) + ")", fg=COLOR_ROJO)
            return

        mapa_atacante[f][c] = tipo
        dinero_actual_atacante = dinero_actual_atacante - costo
        unidades_colocadas.append({"tipo": tipo, "posicion": (f, c)})
        lbl_dinero.config(text="$" + str(dinero_actual_atacante))
        lbl_msg.config(text=unidades_faccion[tipo]["nombre"] + " placed - Cost: $" + str(costo), fg=COLOR_VERDE)
        dibujar_mapa()

    # Cuando el mouse pasa por encima de una casilla, le dibuja un borde
    def hover_celda(event):
        c = (event.x - GRID_X) // CELDA
        f = (event.y - GRID_Y) // CELDA
        canvas.delete("hover")
        if 0 <= f < FILAS and 0 <= c < COLUMNAS and mapa_atacante[f][c] != "base":
            x1 = GRID_X + c * CELDA
            y1 = GRID_Y + f * CELDA
            canvas.create_rectangle(x1, y1, x1 + CELDA, y1 + CELDA, outline=COLOR_1, width=2, tags="hover")

    def borrar_hover(event):
        canvas.delete("hover")

    canvas.bind("<Button-1>", click_celda)
    canvas.bind("<Motion>", hover_celda)
    canvas.bind("<Leave>", borrar_hover)

    # Display de dinero
    lbl_dinero = tk.Label(frame, text="$" + str(dinero_actual_atacante), font=("Courier New", 14, "bold"),
                           bg="#111111", fg=COLOR_1, padx=10, pady=5)
    lbl_dinero.place(x=10, y=10)

    # Display de facción
    tk.Label(frame, text="Attacker - " + faccion, font=("Courier New", 12, "bold"),
              bg="#111111", fg=COLOR_VERDE, padx=10, pady=5).place(x=10, y=50)

    # Panel que explica que hace cada tipo de tropa (a la derecha del mapa).
    texto_tipos_tropa = ("TROOP TYPES\n\n"
                          "Reg: normal\n\n"
                          "Fast: low,\nquick\n\n"
                          "Heavy: high,\nslow")
    tk.Label(frame, text=texto_tipos_tropa, font=("Courier New", 7, "bold"),
              bg="#111111", fg=COLOR_2, justify="left", padx=4, pady=4).place(x=ANCHO_MAPA - 10, y=90, anchor="ne")

    # Panel de compra
    Y_PANEL = GRID_Y + FILAS * CELDA + 8
    botones_ref = {}

    # Cuando el jugador hace click en un boton de unidad (o en Clear)
    def seleccionar_unidad(tipo, btn):
        global tipo_seleccionado_atacante
        tipo_seleccionado_atacante = tipo
        if tipo != "limpiar":
            nombre = unidades_faccion[tipo]["nombre"]
        else:
            nombre = "Clear"
        lbl_msg.config(text="Selected: " + nombre + " - Click the left column to place it")
        for t in botones_ref:
            botones_ref[t].config(relief="flat")
        btn.config(relief="sunken")

    total_ancho = len(unidades_faccion) * 130 + (len(unidades_faccion) - 1) * 10
    x_inicio = (ANCHO_MAPA - total_ancho) // 2

    i = 0
    for tipo in unidades_faccion:
        datos = unidades_faccion[tipo]
        x = x_inicio + i * 140

        # Texto del tipo de tropa que se muestra en el boton (Reg, Fast o Heavy)
        if datos["tipo_tropa"] == "regular":
            texto_tipo = "Reg"
        elif datos["tipo_tropa"] == "rapida":
            texto_tipo = "Fast"
        else:
            texto_tipo = "Heavy"

        # El nombre va en la primera linea, y el precio + tipo en la segunda
        # (si se pone todo junto el boton queda muy ancho y se encima con el de al lado)
        txt = datos["nombre"] + "\n$" + str(datos["costo"]) + " - " + texto_tipo

        imagen_btn = imagen_de_unidad(tipo)

        if imagen_btn:
            # si el boton tiene "image", Tkinter empieza a medir "width"
            # en pixeles en vez de caracteres. Por eso aqui NO se pone width=11
            # (eso lo dejaria muy angosto); se deja que el boton mida lo que necesite.
            btn = tk.Button(frame, text=txt, image=imagen_btn, compound="top", font=FUENTE_SMALL,
                             bg=COLOR_UNIDAD, fg="#0A1628", relief="flat", cursor="hand2", pady=3)
        else:
            btn = tk.Button(frame, text=txt, font=FUENTE_SMALL, bg=COLOR_UNIDAD, fg="#0A1628",
                             relief="flat", cursor="hand2", width=11, pady=3)
        btn.place(x=x, y=Y_PANEL)
        botones_ref[tipo] = btn

        def click_boton_unidad(t=tipo, b=btn):
            seleccionar_unidad(t, b)

        btn.config(command=click_boton_unidad)
        i = i + 1

    # Botón limpiar
    def click_boton_limpiar():
        seleccionar_unidad("limpiar", btn_limpiar)

    x_limpiar = x_inicio + len(unidades_faccion) * 140
    btn_limpiar = tk.Button(frame, text="Clear", font=FUENTE_SMALL, bg=COLOR_ROJO, fg="#FFFFFF",
                             relief="flat", cursor="hand2", width=9, pady=3)
    btn_limpiar.place(x=x_limpiar, y=Y_PANEL)
    botones_ref["limpiar"] = btn_limpiar
    btn_limpiar.config(command=click_boton_limpiar)


    lbl_msg = tk.Label(frame, text="Select a unit and place it in the left column (IN)",
                        font=FUENTE_SMALL, bg="#111111", fg=COLOR_2, padx=10, pady=5)
    lbl_msg.place(x=ANCHO_MAPA // 2, y=10, anchor="n")

    # Botón terminar turno
    def terminar_turno():
        on_turno_listo(unidades_colocadas)

    tk.Button(frame, text="End Turn", font=FUENTE_BTN, bg=COLOR_VERDE, fg="#0A1628",
              relief="flat", cursor="hand2", padx=15, pady=5,
              command=terminar_turno).place(x=ANCHO_MAPA - 10, y=10, anchor="ne")

    dibujar_mapa()
