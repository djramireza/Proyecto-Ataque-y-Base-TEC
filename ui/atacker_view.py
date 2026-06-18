import tkinter as tk
from constantes import *

# Catálogo de unidades por facción
UNIDADES_POR_FACCION = {
    "Madagascar": {
        "pinguino": {"nombre": "Penguin", "costo": 40, "hp": 80, "daño": 10, "velocidad": 1, "img": None},
        "moto_moto": {"nombre": "Moto Moto", "costo": 120, "hp": 200, "daño": 15, "velocidad": 0.5, "img": None},
        "pinguino_negro": {"nombre": "Black Penguin", "costo": 60, "hp": 50, "daño": 5, "velocidad": 2, "img": None},
    },
    "Argentina": {
        "messi": {"nombre": "Messi", "costo": 120, "hp": 100, "daño": 20, "velocidad": 2, "img": None},
        "cerati": {"nombre": "Gustavo Cerati", "costo": 60, "hp": 80, "daño": 10, "velocidad": 1, "img": None},
        "che": {"nombre": "El Che", "costo": 40, "hp": 200, "daño": 8, "velocidad": 0.5, "img": None},
    },
    "India": {
        "tech_support": {"nombre": "Tech Support", "costo": 40, "hp": 80, "daño": 10, "velocidad": 1, "img": None},
        "taxista": {"nombre": "Taxi Driver", "costo": 60, "hp": 50, "daño": 5, "velocidad": 2, "img": None},
        "scammer": {"nombre": "Scammer", "costo": 120, "hp": 100, "daño": 20, "velocidad": 1.5, "img": None},
    },
}

# Etiquetas de texto placeholder por unidad (se reemplaza por imagen más adelante)
ETIQUETAS = {
    "pinguino": "PNG", "moto_moto": "MOTO", "pinguino_negro": "PNG2",
    "messi": "MESSI", "cerati": "CER", "che": "CHE",
    "tech_support": "TECH", "taxista": "TAXI", "scammer": "SCAM",
}

# Variables globales con el estado de la pantalla de ataque
mapa_atacante = []
dinero_actual_atacante = 0
tipo_seleccionado_atacante = None
unidades_colocadas = []


def mostrar_mapa_atacante(root, img_fondo, faccion, faccion_defensor, dinero_inicial, on_turno_listo):
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

                if contenido == "base":
                    canvas.create_text(cx, cy, text="BASE", font=("Arial", 10, "bold"),
                                        fill=color_de_texto(fill), tags="mapa")
                elif contenido in unidades_faccion:
                    etiqueta = ETIQUETAS.get(contenido, "UNI")
                    canvas.create_text(cx, cy, text=etiqueta, font=("Arial", 9, "bold"), tags="mapa")
                elif c == 0:
                    canvas.create_text(cx, cy, text="IN", font=("Arial", 11, "bold"), fill=COLOR_VERDE, tags="mapa")

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

    def hover_celda(event):
        c = (event.x - GRID_X) // CELDA
        f = (event.y - GRID_Y) // CELDA
        canvas.delete("hover")
        if 0 <= f < FILAS and 0 <= c < COLUMNAS and mapa_atacante[f][c] != "base":
            x1 = GRID_X + c * CELDA
            y1 = GRID_Y + f * CELDA
            canvas.create_rectangle(x1, y1, x1 + CELDA, y1 + CELDA, outline=COLOR_1, width=2, tags="hover")

    canvas.bind("<Button-1>", click_celda)
    canvas.bind("<Motion>", hover_celda)
    canvas.bind("<Leave>", lambda e: canvas.delete("hover"))

    # Display de dinero
    lbl_dinero = tk.Label(frame, text="$" + str(dinero_actual_atacante), font=("Courier New", 14, "bold"),
                           bg="#111111", fg=COLOR_1, padx=10, pady=5)
    lbl_dinero.place(x=10, y=10)

    # Display de facción
    tk.Label(frame, text="Attacker - " + faccion, font=("Courier New", 12, "bold"),
              bg="#111111", fg=COLOR_VERDE, padx=10, pady=5).place(x=10, y=50)

    # Panel de compra
    Y_PANEL = GRID_Y + FILAS * CELDA + 8
    botones_ref = {}

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
        txt = datos["nombre"] + "\n$" + str(datos["costo"])
        btn = tk.Button(frame, text=txt, font=FUENTE_SMALL, bg=COLOR_UNIDAD, fg="#0A1628",
                         relief="flat", cursor="hand2", width=11, pady=3)
        btn.place(x=x, y=Y_PANEL)
        botones_ref[tipo] = btn
        btn.config(command=lambda t=tipo, b=btn: seleccionar_unidad(t, b))
        i = i + 1

    # Botón limpiar
    x_limpiar = x_inicio + len(unidades_faccion) * 140
    btn_limpiar = tk.Button(frame, text="Clear", font=FUENTE_SMALL, bg=COLOR_ROJO, fg="#FFFFFF",
                             relief="flat", cursor="hand2", width=9, pady=3)
    btn_limpiar.place(x=x_limpiar, y=Y_PANEL)
    botones_ref["limpiar"] = btn_limpiar
    btn_limpiar.config(command=lambda: seleccionar_unidad("limpiar", btn_limpiar))

    # Mensaje feedback
    lbl_msg = tk.Label(frame, text="Select a unit and place it in the left column (IN)",
                        font=FUENTE_SMALL, bg=COLOR_FONDO, fg=COLOR_2)
    lbl_msg.place(x=ANCHO_MAPA // 2, y=Y_PANEL + 55, anchor="n")

    # Botón terminar turno
    def terminar_turno():
        on_turno_listo(unidades_colocadas)

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
    root.title("Attacker Turn")
    root.resizable(False, False)

    img_fondo = ImageTk.PhotoImage(
        Image.open(os.path.join(folder, "game_bg.png")).resize((ANCHO_MAPA, ALTO_MAPA), Image.LANCZOS)
    )

    def turno_listo(unidades):
        print("Attacker finished:", unidades)

    mostrar_mapa_atacante(root, img_fondo=img_fondo, faccion="Madagascar", faccion_defensor="Argentina",
                           dinero_inicial=200, on_turno_listo=turno_listo)
    root.mainloop()
