import tkinter as tk
from constantes import *

# Pantalla de combate.


ETIQUETAS_TORRE = {"basica": "BAS", "pesada": "PES", "magica": "MAG"}

# Variables globales con el estado de la animación
indice_frame_actual = 0
combate_terminado = False


def mostrar_combate(root, img_fondo, img_base, faccion_defensor, frames, resultado, on_continuar=None):
    global indice_frame_actual, combate_terminado

    root.geometry(str(ANCHO_MAPA) + "x" + str(ALTO_MAPA))

    colores = FACCION_COLORES.get(faccion_defensor, FACCION_COLORES[FACCIONES[0]])
    indice_frame_actual = 0
    combate_terminado = False

    # Interfaz
    frame = tk.Frame(root, bg=COLOR_FONDO)
    frame.place(x=0, y=0, width=ANCHO_MAPA, height=ALTO_MAPA)

    canvas = tk.Canvas(frame, width=ANCHO_MAPA, height=ALTO_MAPA, highlightthickness=0, bg=COLOR_FONDO)
    canvas.place(x=0, y=0)
    canvas.create_image(0, 0, anchor="nw", image=img_fondo)

    # Encabezado: vida de la base
    lbl_base_hp = tk.Label(frame, font=("Courier New", 12, "bold"), bg="#111111", fg=COLOR_1, padx=10, pady=5)
    lbl_base_hp.place(x=10, y=10)

    lbl_turno = tk.Label(frame, font=("Courier New", 11, "bold"), bg="#111111", fg=COLOR_2, padx=10, pady=5)
    lbl_turno.place(x=10, y=50)

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
        dibujar_barra_vida(cx, cy - CELDA // 2 - 12, snapshot.get("base_hp", 0), BASE_HP)

        # Muros
        for muro in snapshot.get("muros", []):
            f, c = muro["posicion"]
            cx, cy = celda_centro(f, c)
            canvas.create_rectangle(cx - CELDA // 2, cy - CELDA // 2, cx + CELDA // 2, cy + CELDA // 2,
                                     fill=colores["muro"], outline="#FFFFFF", tags="combate")
            canvas.create_text(cx, cy, text="WALL", font=("Arial", 9, "bold"),
                                fill=color_de_texto(colores["muro"]), tags="combate")
            dibujar_barra_vida(cx, cy - CELDA // 2 - 10, muro["hp"], muro.get("hp_max", MURO_HP))

        # Torres
        for torre in snapshot.get("torres", []):
            f, c = torre["posicion"]
            cx, cy = celda_centro(f, c)
            clave = "torre_" + torre["tipo"]
            if clave in colores:
                fill_torre = colores[clave]
            else:
                fill_torre = COLOR_TORRE
            canvas.create_rectangle(cx - CELDA // 2, cy - CELDA // 2, cx + CELDA // 2, cy + CELDA // 2,
                                     fill=fill_torre, outline="#FFFFFF", tags="combate")
            etiqueta = ETIQUETAS_TORRE.get(torre["tipo"], "TOR")
            canvas.create_text(cx, cy, text=etiqueta, font=("Arial", 10, "bold"),
                                fill=color_de_texto(fill_torre), tags="combate")
            dibujar_barra_vida(cx, cy - CELDA // 2 - 10, torre["hp"], torre.get("hp_max", 100))

        # Unidades
        for unidad in snapshot.get("unidades", []):
            f, c = unidad["posicion"]
            cx, cy = celda_centro(f, c)
            canvas.create_oval(cx - CELDA // 2 + 4, cy - CELDA // 2 + 4, cx + CELDA // 2 - 4, cy + CELDA // 2 - 4,
                                fill=COLOR_UNIDAD, outline="#FFFFFF", tags="combate")
            canvas.create_text(cx, cy, text=unidad.get("etiqueta", "UNI"), font=("Arial", 8, "bold"), tags="combate")
            dibujar_barra_vida(cx, cy - CELDA // 2 - 10, unidad["hp"], unidad.get("hp_max", 100))

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
        lbl_turno.config(text="Combat turn " + str(indice_frame_actual + 1) + "/" + str(len(frames)))

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


# Prueba rápida de esta pantalla sola - combate simulado solo para ver la animación.
# El combate real lo calculará core/combat.py.
if __name__ == "__main__":
    from PIL import Image, ImageTk
    import os
    folder = os.path.dirname(__file__)

    root = tk.Tk()
    root.title("Combat")
    root.resizable(False, False)

    img_fondo = ImageTk.PhotoImage(
        Image.open(os.path.join(folder, "game_bg.png")).resize((ANCHO_MAPA, ALTO_MAPA), Image.LANCZOS)
    )
    img_base = None

    def generar_frames_demo():
        torres = [{"tipo": "basica", "posicion": (4, 10), "hp": 100, "hp_max": 100}]
        muros = [{"posicion": (4, 6), "hp": MURO_HP, "hp_max": MURO_HP}]
        unidades = [
            {"tipo": "messi", "etiqueta": "MESSI", "posicion": [4, 0], "hp": 100, "hp_max": 100, "daño": 20},
            {"tipo": "che", "etiqueta": "CHE", "posicion": [4, 1], "hp": 200, "hp_max": 200, "daño": 8},
        ]
        base_hp = BASE_HP

        frames = []
        for _ in range(30):
            for u in unidades:
                if u["hp"] <= 0:
                    continue
                f, c = u["posicion"]
                bloqueado = False
                for m in muros:
                    if m["posicion"] == (f, round(c) + 1) and m["hp"] > 0:
                        m["hp"] = m["hp"] - u["daño"]
                        bloqueado = True
                for t in torres:
                    if t["posicion"] == (f, round(c) + 1) and t["hp"] > 0:
                        t["hp"] = t["hp"] - u["daño"]
                        bloqueado = True
                if not bloqueado:
                    if round(c) >= BASE_COL:
                        base_hp = base_hp - u["daño"]
                    else:
                        u["posicion"][1] = u["posicion"][1] + 1

            for t in torres:
                if t["hp"] <= 0:
                    continue
                for u in unidades:
                    if u["hp"] > 0 and abs(u["posicion"][0] - t["posicion"][0]) <= 1:
                        u["hp"] = u["hp"] - 15

            unidades_vivas = []
            for u in unidades:
                if u["hp"] > 0:
                    unidades_vivas.append(dict(u, posicion=tuple(u["posicion"])))

            torres_copia = []
            for t in torres:
                torres_copia.append(dict(t))

            muros_copia = []
            for m in muros:
                muros_copia.append(dict(m))

            frames.append({
                "torres": torres_copia,
                "muros": muros_copia,
                "unidades": unidades_vivas,
                "base_hp": base_hp,
            })

            todas_muertas = True
            for u in unidades:
                if u["hp"] > 0:
                    todas_muertas = False

            if base_hp <= 0 or todas_muertas:
                break

        if base_hp <= 0:
            ganador = "atacante"
        else:
            ganador = "defensor"
        resultado = {"ganador": ganador, "base_hp": base_hp}
        return frames, resultado

    frames_demo, resultado_demo = generar_frames_demo()

    def cuando_termina(resultado):
        print("Combat finished:", resultado)

    mostrar_combate(root, img_fondo, img_base, "Argentina", frames_demo, resultado_demo,
                     on_continuar=cuando_termina)
    root.mainloop()
