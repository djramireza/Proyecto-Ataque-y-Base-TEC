import tkinter as tk
from constantes import *
from defense_view import COOLDOWN_MAXIMO

# Pantalla de combate.


ETIQUETAS_TORRE = {"basica": "🏯", "pesada": "🛡️", "magica": "✨"}

# Variables globales con el estado de la animación
indice_frame_actual = 0
combate_terminado = False


def mostrar_combate(root, img_fondo, img_base, faccion_defensor, frames, resultado,
                     img_messi_arg=None, img_gustavo_arg=None, img_che_arg=None,
                     img_pinguino_madag=None, img_moto_moto_madag=None, img_pinguino_negro_madag=None,
                     img_tech_support_india=None, img_taxi_driver_india=None, img_scammer_india=None,
                     on_continuar=None):
    global indice_frame_actual, combate_terminado

    root.geometry(str(ANCHO_MAPA) + "x" + str(ALTO_MAPA))

    colores = FACCION_COLORES.get(faccion_defensor, FACCION_COLORES[FACCIONES[0]])
    indice_frame_actual = 0
    combate_terminado = False

    # Devuelve la imagen del personaje segun su tipo, o None si no tiene
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

    # Interfaz
    frame = tk.Frame(root, bg=COLOR_FONDO)
    frame.place(x=0, y=0, width=ANCHO_MAPA, height=ALTO_MAPA)

    canvas = tk.Canvas(frame, width=ANCHO_MAPA, height=ALTO_MAPA, highlightthickness=0, bg=COLOR_FONDO)
    canvas.place(x=0, y=0)
    canvas.create_image(0, 0, anchor="nw", image=img_fondo)

    # Encabezado: vida de la base
    lbl_base_hp = tk.Label(frame, font=("Courier New", 12, "bold"), bg="#111111", fg=COLOR_1, padx=10, pady=5)
    lbl_base_hp.place(x=10, y=10)

    def color_barra(ratio):
        if ratio > 0.5:
            return COLOR_VERDE
        elif ratio > 0.2:
            return "#FFC93C"
        else:
            return COLOR_ROJO

    def dibujar_barra_vida(cx, top_y, hp, hp_max, ancho=42):
        if hp < 0:
            hp = 0
        if hp_max:
            ratio = hp / hp_max
        else:
            ratio = 0
        x1 = cx - ancho // 2
        x2 = cx + ancho // 2
        canvas.create_rectangle(x1, top_y, x2, top_y + 6, fill="#222222", outline="#000000", tags="combate")
        canvas.create_rectangle(x1, top_y, x1 + ancho * ratio, top_y + 6,
                                 fill=color_barra(ratio), outline="", tags="combate")

    def celda_centro(f, c):
        x1 = GRID_X + c * CELDA
        y1 = GRID_Y + f * CELDA
        return x1 + CELDA // 2, y1 + CELDA // 2

    def dibujar_grilla():
        for f in range(FILAS):
            for c in range(COLUMNAS):
                x1 = GRID_X + c * CELDA
                y1 = GRID_Y + f * CELDA
                canvas.create_rectangle(x1, y1, x1 + CELDA, y1 + CELDA, outline=COLOR_BORDE, width=1, tags="combate")

    def dibujar_frame(snapshot):
        canvas.delete("combate")
        dibujar_grilla()

        # Base
        cx, cy = celda_centro(BASE_FILA, BASE_COL)
        if img_base:
            canvas.create_image(cx, cy, image=img_base, tags="combate")
        else:
            canvas.create_rectangle(cx - CELDA // 2, cy - CELDA // 2, cx + CELDA // 2, cy + CELDA // 2,
                                     fill=colores["base"], outline="#FFFFFF", tags="combate")
            canvas.create_text(cx, cy, text="BASE", font=("Arial", 10, "bold"),
                                fill=color_de_texto(colores["base"]), tags="combate")
        # La barrita de vida va PEGADA ARRIBA, DENTRO de la propia celda
        # (si se dibuja flotando por encima, se mete en la celda de arriba
        # y cuando esa celda se pinta, la tapa)
        dibujar_barra_vida(cx, cy - CELDA // 2 + 3, snapshot.get("base_hp", 0), BASE_HP)

        # Muros
        for muro in snapshot.get("muros", []):
            f, c = muro["posicion"]
            cx, cy = celda_centro(f, c)
            canvas.create_rectangle(cx - CELDA // 2, cy - CELDA // 2, cx + CELDA // 2, cy + CELDA // 2,
                                     fill=colores["muro"], outline="#FFFFFF", tags="combate")
            canvas.create_text(cx, cy, text="🧱", font=("Segoe UI Emoji", 8),
                                fill=color_de_texto(colores["muro"]), tags="combate")
            dibujar_barra_vida(cx, cy - CELDA // 2 + 3, muro["hp"], muro.get("hp_max", MURO_HP))

        # Torres
        for torre in snapshot.get("torres", []):
            f, c = torre["posicion"]
            cx, cy = celda_centro(f, c)
            clave = "torre_" + torre["tipo"]
            if clave in colores:
                fill_torre = colores[clave]
            else:
                fill_torre = COLOR_TORRE

            # Si la habilidad de la torre se activo justo en este turno,
            # la dibujamos con un borde grueso y brillante (el "parpadeo")
            if torre.get("lista"):
                borde_color = COLOR_1
                borde_ancho = 4
            else:
                borde_color = "#FFFFFF"
                borde_ancho = 1

            canvas.create_rectangle(cx - CELDA // 2, cy - CELDA // 2, cx + CELDA // 2, cy + CELDA // 2,
                                     fill=fill_torre, outline=borde_color, width=borde_ancho, tags="combate")
            etiqueta = ETIQUETAS_TORRE.get(torre["tipo"], "TOR")
            canvas.create_text(cx, cy, text=etiqueta, font=("Arial", 20, "bold"),
                                fill=color_de_texto(fill_torre), tags="combate")

            # La barrita de cooldown va primero (mas arriba) y la de vida
            # debajo, las dos DENTRO de la celda de la torre. Si se dibujan
            # flotando por encima de la celda, se meten en la celda de la
            # torre de arriba y cuando esa se pinta, las tapa.
            if "cooldown" in torre:
                cooldown_max = COOLDOWN_MAXIMO[torre["tipo"]]
                ancho_barra = 36
                x1_b = cx - ancho_barra // 2
                x2_b = cx + ancho_barra // 2
                y_barra = cy - CELDA // 2 + 3
                ancho_lleno = ancho_barra * torre["cooldown"] / cooldown_max

                canvas.create_rectangle(x1_b, y_barra, x2_b, y_barra + 5,
                                         fill="#222222", outline="#000000", tags="combate")
                canvas.create_rectangle(x1_b, y_barra, x1_b + ancho_lleno, y_barra + 5,
                                         fill=COLOR_VERDE, outline="", tags="combate")

            dibujar_barra_vida(cx, cy - CELDA // 2 + 11, torre["hp"], torre.get("hp_max", 100))

        # Unidades
        for unidad in snapshot.get("unidades", []):
            f, c = unidad["posicion"]
            cx, cy = celda_centro(f, c)
            tipo_unidad = unidad.get("tipo")
            imagen_unidad = imagen_de_unidad(tipo_unidad)

            # Si la unidad activo su habilidad justo en este turno, tiene borde que brilla
            if unidad.get("lista"):
                borde_color = COLOR_1
                borde_ancho = 3
            else:
                borde_color = "#FFFFFF"
                borde_ancho = 1

            if imagen_unidad:
                canvas.create_rectangle(cx - CELDA // 2 + 2, cy - CELDA // 2 + 2, cx + CELDA // 2 - 2, cy + CELDA // 2 - 2,
                                         outline=borde_color, width=borde_ancho, tags="combate")
                canvas.create_image(cx, cy, image=imagen_unidad, tags="combate")
            else:
                canvas.create_oval(cx - CELDA // 2 + 4, cy - CELDA // 2 + 4, cx + CELDA // 2 - 4, cy + CELDA // 2 - 4,
                                    fill=COLOR_UNIDAD, outline=borde_color, width=borde_ancho, tags="combate")
                canvas.create_text(cx, cy, text=unidad.get("etiqueta", "UNI"), font=("Arial", 8, "bold"), tags="combate")

            dibujar_barra_vida(cx, cy - CELDA // 2 + 3, unidad["hp"], unidad.get("hp_max", 100))

    def mostrar_resultado():
        global combate_terminado
        combate_terminado = True

        ganador = resultado.get("ganador", "defensor")
        if ganador == "defensor":
            texto = "DEFENDER WINS THE ROUND!"
            color = COLOR_VERDE
        else:
            texto = "ATTACKER WINS THE ROUND!"
            color = COLOR_ROJO

        vida_restante = resultado.get("base_hp", 0)
        if vida_restante < 0:
            vida_restante = 0

        overlay = tk.Frame(frame, bg=COLOR_PANEL, padx=40, pady=30,
                            highlightbackground=COLOR_1, highlightthickness=2)
        overlay.place(x=ANCHO_MAPA // 2, y=ALTO_MAPA // 2, anchor="center")

        tk.Label(overlay, text=texto, font=("Georgia", 22, "bold"), bg=COLOR_PANEL, fg=color).pack(pady=(0, 10))
        tk.Label(overlay, text="Base HP remaining: " + str(vida_restante),
                 font=FUENTE_SMALL, bg=COLOR_PANEL, fg=COLOR_2).pack(pady=(0, 20))

        def continuar():
            if on_continuar:
                on_continuar(resultado)

        tk.Button(overlay, text="Continue", font=FUENTE_BTN, bg=COLOR_1, fg="#0A1628",
                  relief="flat", cursor="hand2", width=20, pady=8, command=continuar).pack()

    DURACION_FRAME_MS = 450

    def siguiente_frame():
        global indice_frame_actual

        if combate_terminado:
            return
        if indice_frame_actual >= len(frames):
            mostrar_resultado()
            return

        snapshot = frames[indice_frame_actual]
        dibujar_frame(snapshot)

        hp_mostrar = snapshot.get("base_hp", 0)
        if hp_mostrar < 0:
            hp_mostrar = 0
        lbl_base_hp.config(text="Base HP: " + str(hp_mostrar) + "/" + str(BASE_HP))

        indice_frame_actual = indice_frame_actual + 1
        root.after(DURACION_FRAME_MS, siguiente_frame)

    def saltar_animacion():
        global indice_frame_actual
        indice_frame_actual = len(frames)
        if frames:
            dibujar_frame(frames[-1])
        mostrar_resultado()

    tk.Button(frame, text="Skip animation", font=FUENTE_SMALL, bg=COLOR_PANEL, fg=COLOR_2,
              relief="flat", cursor="hand2", command=saltar_animacion).place(x=ANCHO_MAPA - 10, y=10, anchor="ne")

    if frames:
        siguiente_frame()
    else:
        mostrar_resultado()
