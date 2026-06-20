import os
import sys
import tkinter as tk
from PIL import Image, ImageTk

# Las vistas adentro de ui/ usan imports tipo "from constantes import *" entre ellas,
# así que agregamos la carpeta ui al path para que esos imports internos funcionen.
UI_FOLDER = os.path.join(os.path.dirname(__file__), "ui")
sys.path.insert(0, UI_FOLDER)

# Todas las imagenes del juego estan guardadas en ui/imagenes
IMAGENES_FOLDER = os.path.join(UI_FOLDER, "imagenes")

from ui.constantes import *
from ui.menu_view import mostrar_menu_principal
from ui.leaderboard_view import mostrar_leaderboard
from ui.login_view import mostrar_login
from ui.role_view import mostrar_seleccion_rol
from ui.faction_view import mostrar_facciones
from ui.defense_view import mostrar_mapa_defensor, TORRES, COOLDOWN_MAXIMO
from ui.atacker_view import mostrar_mapa_atacante, UNIDADES_POR_FACCION, ETIQUETAS
from ui.combat_view import mostrar_combate

DINERO_INICIAL = 200
RONDAS_PARA_GANAR = 3

# Variables globales con los datos de los dos jugadores
jugador1_usuario = None
jugador1_rol = None
jugador1_faccion = None

jugador2_usuario = None
jugador2_rol = None
jugador2_faccion = None

victorias_defensor = 0
victorias_atacante = 0


def limpiar_pantalla(root):
    for widget in root.winfo_children():
        widget.destroy()


def jugador_con_rol(rol):
    global jugador1_rol, jugador2_rol
    if jugador1_rol == rol:
        return 1
    elif jugador2_rol == rol:
        return 2
    else:
        return None


def reiniciar_partida():
    global jugador1_usuario, jugador1_rol, jugador1_faccion
    global jugador2_usuario, jugador2_rol, jugador2_faccion
    global victorias_defensor, victorias_atacante

    jugador1_usuario = None
    jugador1_rol = None
    jugador1_faccion = None
    jugador2_usuario = None
    jugador2_rol = None
    jugador2_faccion = None
    victorias_defensor = 0
    victorias_atacante = 0


# Combate de relleno temporal hasta que Romu suba combat.py.
# Solo hace avanzar las unidades en línea recta y resta vida a torres/muros/base.
def simular_combate_temporal(objetos_defensa, unidades_ataque, faccion_atacante):
    catalogo_unidades = UNIDADES_POR_FACCION[faccion_atacante]

    torres = []
    muros = []
    for o in objetos_defensa:
        if o["tipo"] == "muro":
            muros.append({"posicion": o["posicion"], "hp": MURO_HP, "hp_max": MURO_HP})
        else:
            datos = TORRES[o["tipo"]]
            # "cooldown" cuenta los turnos hasta activar la habilidad de la torre.
            # "lista" marca el turno exacto en el que la habilidad se activa
            # (para que combat_view.py la haga "brillar" justo en ese frame).
            torres.append({"tipo": o["tipo"], "posicion": o["posicion"], "hp": datos["hp"], "hp_max": datos["hp"],
                           "cooldown": 0, "lista": False})

    unidades = []
    for u in unidades_ataque:
        datos = catalogo_unidades[u["tipo"]]
        etiqueta = ETIQUETAS.get(u["tipo"], "UNI")
        unidades.append({
            "tipo": u["tipo"], "etiqueta": etiqueta, "posicion": list(u["posicion"]),
            "hp": datos["hp"], "hp_max": datos["hp"], "daño": datos["daño"],
        })

    base_hp = BASE_HP
    frames = []

    for _ in range(40):
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

        # Cada turno, las torres con vida avanzan el cooldown de su habilidad.
        # Cuando llega al maximo, se reinicia y se marca "lista" por un solo
        # turno; eso es lo que hace que combat_view.py la muestre brillando.
        for t in torres:
            if t["hp"] <= 0:
                t["lista"] = False
                continue
            maximo = COOLDOWN_MAXIMO[t["tipo"]]
            t["cooldown"] = t["cooldown"] + 1
            if t["cooldown"] >= maximo:
                t["cooldown"] = 0
                t["lista"] = True
            else:
                t["lista"] = False

        torres_copia = []
        for t in torres:
            torres_copia.append(dict(t))

        muros_copia = []
        for m in muros:
            muros_copia.append(dict(m))

        unidades_vivas = []
        for u in unidades:
            if u["hp"] > 0:
                unidades_vivas.append(dict(u, posicion=tuple(u["posicion"])))

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

    return frames, {"ganador": ganador, "base_hp": base_hp}


def main():
    root = tk.Tk()
    root.title("Base Defense and Assault")
    root.resizable(False, False)
    root.geometry(str(ANCHO) + "x" + str(ALTO))

    img_menu_bg = ImageTk.PhotoImage(Image.open(os.path.join(IMAGENES_FOLDER, "menu_bg_night.png")).resize((ANCHO, ALTO)))
    img_madagascar = ImageTk.PhotoImage(Image.open(os.path.join(IMAGENES_FOLDER, "madagascar_fc.png")).resize((200, 200)))
    img_argentina = ImageTk.PhotoImage(Image.open(os.path.join(IMAGENES_FOLDER, "argentina_fc.png")).resize((200, 200)))
    img_india = ImageTk.PhotoImage(Image.open(os.path.join(IMAGENES_FOLDER, "india_fc.png")).resize((200, 200)))
    img_mapa_bg = ImageTk.PhotoImage(Image.open(os.path.join(IMAGENES_FOLDER, "game_bg.png")).resize((ANCHO_MAPA, ALTO_MAPA)))

    # Imagenes de los personajes de cada faccion (se usan en defensa, ataque y combate)
    # Son fotos en formato retrato, no cuadradas, asi que mantenemos su proporcion
    # original y solo las achicamos a una altura fija para que no se vean estiradas.
    img_messi_arg = ImageTk.PhotoImage(Image.open(os.path.join(IMAGENES_FOLDER, "messi_arg.png")).resize((41, 50)))
    img_gustavo_arg = ImageTk.PhotoImage(Image.open(os.path.join(IMAGENES_FOLDER, "gustavo_arg.png")).resize((35, 50)))
    img_che_arg = ImageTk.PhotoImage(Image.open(os.path.join(IMAGENES_FOLDER, "che_arg.png")).resize((26, 50)))

    img_pinguino_madag = ImageTk.PhotoImage(Image.open(os.path.join(IMAGENES_FOLDER, "pengui_madag.png")).resize((39, 50)))
    img_moto_moto_madag = ImageTk.PhotoImage(Image.open(os.path.join(IMAGENES_FOLDER, "moto_moto_madag.png")).resize((40, 50)))
    img_pinguino_negro_madag = ImageTk.PhotoImage(Image.open(os.path.join(IMAGENES_FOLDER, "pingui_negro_madag.png")).resize((38, 50)))

    img_tech_support_india = ImageTk.PhotoImage(Image.open(os.path.join(IMAGENES_FOLDER, "techsupport_india.png")).resize((36, 50)))
    img_taxi_driver_india = ImageTk.PhotoImage(Image.open(os.path.join(IMAGENES_FOLDER, "taxi_driver_india.png")).resize((39, 50)))
    img_scammer_india = ImageTk.PhotoImage(Image.open(os.path.join(IMAGENES_FOLDER, "scammer_india.png")).resize((35, 50)))

    # Menu principal
    def comenzar_juego():
        iniciar_login(1)

    def iniciar_menu():
        limpiar_pantalla(root)
        root.geometry(str(ANCHO) + "x" + str(ALTO))
        mostrar_menu_principal(root, img_menu_bg, on_comenzar=comenzar_juego,
                                on_ver_leaderboard=iniciar_leaderboard, on_salir=root.destroy)

    def iniciar_leaderboard():
        limpiar_pantalla(root)
        root.geometry(str(ANCHO) + "x" + str(ALTO))
        mostrar_leaderboard(root, img_menu_bg, on_volver=iniciar_menu)

    # Paso 1: login de los dos jugadores
    def iniciar_login(numero_jugador):
        limpiar_pantalla(root)
        root.geometry(str(ANCHO) + "x" + str(ALTO))

        def cuando_login_exitoso(datos):
            cuando_loguea(numero_jugador, datos)

        mostrar_login(root, img_menu_bg, numero_jugador=numero_jugador,
                      on_success=cuando_login_exitoso)

    def cuando_loguea(numero_jugador, datos):
        global jugador1_usuario, jugador2_usuario
        if numero_jugador == 1:
            jugador1_usuario = datos.get("usuario")
            iniciar_login(2)
        else:
            jugador2_usuario = datos.get("usuario")
            iniciar_rol(1)

    # Paso 2: selección de rol
    def iniciar_rol(numero_jugador, rol_tomado=None):
        limpiar_pantalla(root)

        def cuando_se_elige_rol(rol):
            cuando_elige_rol(numero_jugador, rol)

        mostrar_seleccion_rol(root, img_menu_bg, numero_jugador=numero_jugador, rol_tomado=rol_tomado,
                               on_success=cuando_se_elige_rol)

    def cuando_elige_rol(numero_jugador, rol):
        global jugador1_rol, jugador2_rol
        if numero_jugador == 1:
            jugador1_rol = rol
            iniciar_rol(2, rol_tomado=rol)
        else:
            jugador2_rol = rol
            iniciar_faccion(1)

    # Paso 3: selección de facción
    def iniciar_faccion(numero_jugador, faccion_tomada=None):
        limpiar_pantalla(root)

        def cuando_se_elige_faccion(faccion):
            cuando_elige_faccion(numero_jugador, faccion)

        mostrar_facciones(root, img_menu_bg, img_madagascar, img_argentina, img_india,
                           numero_jugador=numero_jugador, faccion_tomada=faccion_tomada,
                           on_success=cuando_se_elige_faccion)

    def cuando_elige_faccion(numero_jugador, faccion):
        global jugador1_faccion, jugador2_faccion
        if numero_jugador == 1:
            jugador1_faccion = faccion
            iniciar_faccion(2, faccion_tomada=faccion)
        else:
            jugador2_faccion = faccion
            iniciar_ronda()

    # Ronda: construir defensa, construir ataque, combate
    def iniciar_ronda():
        num_defensor = jugador_con_rol("defensor")
        num_atacante = jugador_con_rol("atacante")

        if num_defensor == 1:
            faccion_defensor = jugador1_faccion
        else:
            faccion_defensor = jugador2_faccion

        if num_atacante == 1:
            faccion_atacante = jugador1_faccion
        else:
            faccion_atacante = jugador2_faccion

        limpiar_pantalla(root)

        def cuando_defensa_lista(objetos):
            cuando_termina_defensa(objetos, faccion_defensor, faccion_atacante)

        mostrar_mapa_defensor(root, img_mapa_bg, None, faccion_defensor,
                               dinero_inicial=DINERO_INICIAL,
                               on_turno_listo=cuando_defensa_lista,
                               faccion_atacante=faccion_atacante,
                               img_messi_arg=img_messi_arg, img_gustavo_arg=img_gustavo_arg, img_che_arg=img_che_arg,
                               img_pinguino_madag=img_pinguino_madag, img_moto_moto_madag=img_moto_moto_madag,
                               img_pinguino_negro_madag=img_pinguino_negro_madag,
                               img_tech_support_india=img_tech_support_india, img_taxi_driver_india=img_taxi_driver_india,
                               img_scammer_india=img_scammer_india)

    def cuando_termina_defensa(objetos_defensa, faccion_defensor, faccion_atacante):
        limpiar_pantalla(root)

        def cuando_ataque_listo(unidades):
            cuando_termina_ataque(objetos_defensa, unidades, faccion_defensor, faccion_atacante)

        mostrar_mapa_atacante(root, img_mapa_bg, faccion_atacante, faccion_defensor,
                               dinero_inicial=DINERO_INICIAL,
                               on_turno_listo=cuando_ataque_listo,
                               img_messi_arg=img_messi_arg, img_gustavo_arg=img_gustavo_arg, img_che_arg=img_che_arg,
                               img_pinguino_madag=img_pinguino_madag, img_moto_moto_madag=img_moto_moto_madag,
                               img_pinguino_negro_madag=img_pinguino_negro_madag,
                               img_tech_support_india=img_tech_support_india, img_taxi_driver_india=img_taxi_driver_india,
                               img_scammer_india=img_scammer_india)

    def cuando_termina_ataque(objetos_defensa, unidades_ataque, faccion_defensor, faccion_atacante):
        # TODO: reemplazar por el motor real de core/combat.py cuando esté listo
        frames, resultado = simular_combate_temporal(objetos_defensa, unidades_ataque, faccion_atacante)
        limpiar_pantalla(root)
        mostrar_combate(root, img_mapa_bg, None, faccion_defensor, frames, resultado,
                         img_messi_arg=img_messi_arg, img_gustavo_arg=img_gustavo_arg, img_che_arg=img_che_arg,
                         img_pinguino_madag=img_pinguino_madag, img_moto_moto_madag=img_moto_moto_madag,
                         img_pinguino_negro_madag=img_pinguino_negro_madag,
                         img_tech_support_india=img_tech_support_india, img_taxi_driver_india=img_taxi_driver_india,
                         img_scammer_india=img_scammer_india,
                         on_continuar=cuando_termina_combate)

    def cuando_termina_combate(resultado):
        global victorias_defensor, victorias_atacante
        if resultado["ganador"] == "defensor":
            victorias_defensor = victorias_defensor + 1
        else:
            victorias_atacante = victorias_atacante + 1

        if victorias_defensor >= RONDAS_PARA_GANAR or victorias_atacante >= RONDAS_PARA_GANAR:
            mostrar_fin()
        else:
            iniciar_ronda()

    # Fin de partida
    def mostrar_fin():
        limpiar_pantalla(root)
        root.geometry(str(ANCHO_MAPA) + "x" + str(ALTO_MAPA))

        if victorias_defensor > victorias_atacante:
            ganador = "DEFENDER"
        else:
            ganador = "ATTACKER"

        frame = tk.Frame(root, bg=COLOR_FONDO)
        frame.place(x=0, y=0, width=ANCHO_MAPA, height=ALTO_MAPA)
        tk.Label(frame, text=ganador + " WINS THE GAME", font=FUENTE_TITULO,
                 bg=COLOR_FONDO, fg=COLOR_1).pack(pady=(220, 10))
        tk.Label(frame, text="Defender " + str(victorias_defensor) + " - " + str(victorias_atacante) + " Attacker",
                 font=FUENTE_BTN, bg=COLOR_FONDO, fg=COLOR_2).pack(pady=(0, 30))
        tk.Button(frame, text="Play again", font=FUENTE_BTN, bg=COLOR_1, fg="#0A1628",
                  relief="flat", cursor="hand2", width=20, pady=8, command=jugar_de_nuevo).pack()

    def jugar_de_nuevo():
        reiniciar_partida()
        iniciar_menu()

    iniciar_menu()
    root.mainloop()


if __name__ == "__main__":
    main()
