import os
import sys
import tkinter as tk
from PIL import Image, ImageTk

# Las vistas adentro de ui/ usan imports tipo "from constantes import *" entre ellas,
# así que agregamos la carpeta ui al path para que esos imports internos funcionen.
UI_FOLDER = os.path.join(os.path.dirname(__file__), "ui")
sys.path.insert(0, UI_FOLDER)

# Lo mismo para core/: sus archivos se importan entre si con "from entities import ..."
# en vez de "from core.entities import ...", asi que core tambien va al path.
CORE_FOLDER = os.path.join(os.path.dirname(__file__), "core")
sys.path.insert(0, CORE_FOLDER)

# Todas las imagenes del juego estan guardadas en ui/imagenes
IMAGENES_FOLDER = os.path.join(UI_FOLDER, "imagenes")

from ui.constantes import *
from ui.menu_view import mostrar_menu_principal
from ui.leaderboard_view import mostrar_leaderboard
from ui.login_view import mostrar_login
from ui.role_view import mostrar_seleccion_rol
from ui.faction_view import mostrar_facciones
from ui.defense_view import mostrar_mapa_defensor
from ui.atacker_view import mostrar_mapa_atacante, UNIDADES_POR_FACCION, ETIQUETAS, TIPO_TROPA_A_GENERICO
from ui.combat_view import mostrar_combate

from core.data_manager import actualizar_victoria
from core.entities import Tower, Unidad, Pared, Base
from core.data_definitions import TOWERS_CATALOG, UNITS_CATALOG
from core.economy import COSTO_PARED, HP_PARED, DINERO_INICIAL, DINERO_POR_RONDA, RONDAS_PARA_GANAR
from core.combat import CombatEngine

# Variables globales con los datos de los dos jugadores
jugador1_usuario = None
jugador1_rol = None
jugador1_faccion = None

jugador2_usuario = None
jugador2_rol = None
jugador2_faccion = None

victorias_defensor = 0
victorias_atacante = 0

# Dinero del defensor y del atacante. Le pertenece al rol, no al jugador, porque el rol
# de cada jugador no cambia durante la partida (solo cambia de ronda en ronda el mapa).
dinero_defensor = DINERO_INICIAL
dinero_atacante = DINERO_INICIAL


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
    global dinero_defensor, dinero_atacante

    jugador1_usuario = None
    jugador1_rol = None
    jugador1_faccion = None
    jugador2_usuario = None
    jugador2_rol = None
    jugador2_faccion = None
    victorias_defensor = 0
    victorias_atacante = 0
    dinero_defensor = DINERO_INICIAL
    dinero_atacante = DINERO_INICIAL


# Construye las entidades reales del core (Tower/Pared/Unidad/Base) a partir de lo que
# colocaron el defensor y el atacante en sus pantallas, y corre el motor de combate real.
def ejecutar_combate_real(objetos_defensa, unidades_ataque, faccion_atacante):
    catalogo_unidades = UNIDADES_POR_FACCION[faccion_atacante]

    torres = []
    paredes = []
    for o in objetos_defensa:
        if o["tipo"] == "muro":
            pared = Pared(coste=COSTO_PARED, hp=HP_PARED)
            pared.position = o["posicion"]
            paredes.append(pared)
        else:
            torre = Tower(**TOWERS_CATALOG[o["tipo"]])
            torre.position = o["posicion"]
            torre.tipo = o["tipo"]
            torres.append(torre)

    unidades = []
    for u in unidades_ataque:
        tipo_tropa = catalogo_unidades[u["tipo"]]["tipo_tropa"]
        clave_generica = TIPO_TROPA_A_GENERICO[tipo_tropa]
        unidad = Unidad(**UNITS_CATALOG[clave_generica])
        unidad.position = tuple(u["posicion"])
        unidad.tipo = u["tipo"]
        unidad.etiqueta = ETIQUETAS.get(u["tipo"], "UNI")
        unidades.append(unidad)

    base = Base(hp=BASE_HP, position=(BASE_FILA, BASE_COL))

    motor = CombatEngine(towers=torres, paredes=paredes, unidades=unidades, base=base)
    frames, resultado_core = motor.ejecutar_ronda()

    resultado = {
        "ganador": resultado_core["ganador"],
        "base_hp": resultado_core["base_hp_restante"],
        "dinero_defensor_ganado": resultado_core["dinero_defensor"],
        "dinero_atacante_ganado": resultado_core["dinero_atacante"],
    }
    return frames, resultado


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
        global dinero_defensor, dinero_atacante

        # Al inicio de cada ronda se suma una cantidad fija de dinero a ambos jugadores,
        # encima de lo que ya tenian acumulado (ahorros de rondas anteriores).
        dinero_defensor = dinero_defensor + DINERO_POR_RONDA
        dinero_atacante = dinero_atacante + DINERO_POR_RONDA

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

        def cuando_defensa_lista(objetos, dinero_restante):
            global dinero_defensor
            # Lo que no se gastó construyendo no se pierde, pasa a la fase de ataque
            # y a la próxima ronda como parte del dinero del defensor.
            dinero_defensor = dinero_restante
            cuando_termina_defensa(objetos, faccion_defensor, faccion_atacante)

        mostrar_mapa_defensor(root, img_mapa_bg, None, faccion_defensor,
                               dinero_inicial=dinero_defensor,
                               on_turno_listo=cuando_defensa_lista,
                               faccion_atacante=faccion_atacante,
                               img_messi_arg=img_messi_arg, img_gustavo_arg=img_gustavo_arg, img_che_arg=img_che_arg,
                               img_pinguino_madag=img_pinguino_madag, img_moto_moto_madag=img_moto_moto_madag,
                               img_pinguino_negro_madag=img_pinguino_negro_madag,
                               img_tech_support_india=img_tech_support_india, img_taxi_driver_india=img_taxi_driver_india,
                               img_scammer_india=img_scammer_india)

    def cuando_termina_defensa(objetos_defensa, faccion_defensor, faccion_atacante):
        limpiar_pantalla(root)

        def cuando_ataque_listo(unidades, dinero_restante):
            global dinero_atacante
            # Lo que no se gastó comprando unidades no se pierde, queda guardado
            # para sumarle lo que se gane en el combate de esta ronda.
            dinero_atacante = dinero_restante
            cuando_termina_ataque(objetos_defensa, unidades, faccion_defensor, faccion_atacante)

        mostrar_mapa_atacante(root, img_mapa_bg, faccion_atacante, faccion_defensor,
                               dinero_inicial=dinero_atacante,
                               on_turno_listo=cuando_ataque_listo,
                               img_messi_arg=img_messi_arg, img_gustavo_arg=img_gustavo_arg, img_che_arg=img_che_arg,
                               img_pinguino_madag=img_pinguino_madag, img_moto_moto_madag=img_moto_moto_madag,
                               img_pinguino_negro_madag=img_pinguino_negro_madag,
                               img_tech_support_india=img_tech_support_india, img_taxi_driver_india=img_taxi_driver_india,
                               img_scammer_india=img_scammer_india)

    def cuando_termina_ataque(objetos_defensa, unidades_ataque, faccion_defensor, faccion_atacante):
        global dinero_defensor, dinero_atacante

        frames, resultado = ejecutar_combate_real(objetos_defensa, unidades_ataque, faccion_atacante)

        # El defensor gana dinero por cada unidad enemiga eliminada, y el atacante gana
        # dinero por el daño que le hizo a torres y a la base durante el combate. Ese
        # dinero queda guardado para la proxima ronda.
        dinero_defensor = dinero_defensor + resultado["dinero_defensor_ganado"]
        dinero_atacante = dinero_atacante + resultado["dinero_atacante_ganado"]

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
            registrar_victoria_partida(resultado["ganador"])
            mostrar_fin()
        else:
            iniciar_ronda()

    # Guarda en data/players.json la victoria del jugador que ganó la partida completa
    def registrar_victoria_partida(rol_ganador):
        numero_ganador = jugador_con_rol(rol_ganador)
        if numero_ganador == 1:
            usuario_ganador = jugador1_usuario
        else:
            usuario_ganador = jugador2_usuario
        actualizar_victoria(usuario_ganador, rol_ganador)

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
