import tkinter as tk
from constantes import *
from core.auth import iniciar_sesion, registrar_jugador
from core.data_manager import obtener_jugador

# Variable global que dice si estamos en modo "login" o modo "registro"
modo = "login"


def hacer_login(usuario, contrasena):
    ok, mensaje = iniciar_sesion(usuario, contrasena)
    if not ok:
        return False, mensaje
    datos_jugador = obtener_jugador(usuario)
    return True, {"victorias_defensor": datos_jugador["wins_defensor"],
                  "victorias_atacante": datos_jugador["wins_atacante"]}


def hacer_registro(usuario, contrasena):
    return registrar_jugador(usuario, contrasena)


def mostrar_login(root, img_fondo, on_success, numero_jugador=1):
    global modo
    modo = "login"

    # Frame principal
    frame = tk.Frame(root, bg=COLOR_FONDO)
    frame.place(x=0, y=0, width=900, height=600)

    # Fondo
    canvas = tk.Canvas(frame, width=900, height=600, highlightthickness=0, bg=COLOR_FONDO)
    canvas.place(x=0, y=0)
    canvas.create_image(0, 0, anchor="nw", image=img_fondo)

    # Título
    canvas.create_text(450, 90, text="TOWER DEFENSE", font=FUENTE_TITULO, fill=COLOR_1)
    canvas.create_text(450, 140, text="Base Defense and Assault", font=FUENTE_SMALL, fill=COLOR_2)

    # Panel de login
    panel = tk.Frame(frame, bg=COLOR_PANEL, padx=36, pady=28,
                      highlightbackground=COLOR_1, highlightthickness=1)
    canvas.create_window(450, 360, window=panel)

    # Título del panel
    lbl_titulo = tk.Label(panel, text="LOG IN - PLAYER " + str(numero_jugador),
                           font=("Courier New", 13, "bold"), bg=COLOR_PANEL, fg=COLOR_1)
    lbl_titulo.grid(row=0, column=0, pady=(0, 18))

    # Usuario
    tk.Label(panel, text="USER", font=FUENTE_LABEL, bg=COLOR_PANEL, fg=COLOR_2).grid(row=1, column=0, sticky="w")
    entry_usuario = tk.Entry(panel, font=FUENTE_ENTRY, width=26, bg="#0A1E38", fg=COLOR_TEXTO,
                              insertbackground=COLOR_TEXTO, relief="flat",
                              highlightbackground=COLOR_1, highlightthickness=1)
    entry_usuario.grid(row=2, column=0, pady=(4, 12))

    # Contraseña
    tk.Label(panel, text="PASSWORD", font=FUENTE_LABEL, bg=COLOR_PANEL, fg=COLOR_2).grid(row=3, column=0, sticky="w")
    entry_contra = tk.Entry(panel, font=FUENTE_ENTRY, width=26, bg="#0A1E38", fg=COLOR_TEXTO,
                             insertbackground=COLOR_TEXTO, relief="flat",
                             highlightbackground=COLOR_1, highlightthickness=1, show="*")
    entry_contra.grid(row=4, column=0, pady=(4, 20))

    # Mensaje de error o de éxito
    lbl_msg = tk.Label(panel, text="", font=FUENTE_SMALL, bg=COLOR_PANEL, fg=COLOR_ROJO, wraplength=260)
    lbl_msg.grid(row=7, column=0, pady=(12, 0))

    def cambiar_modo():
        global modo
        lbl_msg.config(text="")
        if modo == "login":
            modo = "registro"
            lbl_titulo.config(text="CREATE ACCOUNT")
            btn_main.config(text="REGISTER")
            btn_switch.config(text="Already registered? Login")
        else:
            modo = "login"
            lbl_titulo.config(text="LOG IN - PLAYER " + str(numero_jugador))
            btn_main.config(text="ENTER")
            btn_switch.config(text="Don't have an account? Create one")

    def handle_btn():
        usuario = entry_usuario.get().strip()
        contrasena = entry_contra.get().strip()

        if usuario == "" or contrasena == "":
            lbl_msg.config(text="Please fill in everything.", fg=COLOR_ROJO)
            return

        if modo == "login":
            ok, resultado = hacer_login(usuario, contrasena)
            if ok:
                lbl_msg.config(text="Welcome, " + usuario + "!", fg=COLOR_VERDE)
                resultado["usuario"] = usuario

                def avisar_login_exitoso():
                    on_success(resultado)

                frame.after(600, avisar_login_exitoso)
            else:
                lbl_msg.config(text=resultado, fg=COLOR_ROJO)
        else:
            ok, resultado = hacer_registro(usuario, contrasena)
            if ok:
                lbl_msg.config(text="Account created! Please log in.", fg=COLOR_VERDE)
                frame.after(1000, cambiar_modo)
            else:
                lbl_msg.config(text=resultado, fg=COLOR_ROJO)

    # Botón principal
    btn_main = tk.Button(panel, text="ENTER", font=FUENTE_BTN, bg=COLOR_1, fg="#0A1628",
                          relief="flat", cursor="hand2", width=24, pady=7, command=handle_btn)
    btn_main.grid(row=5, column=0, pady=(0, 8))

    # Botón para cambiar entre login y registro
    btn_switch = tk.Button(panel, text="Don't have an account? Create one", font=FUENTE_SMALL,
                            bg=COLOR_PANEL, fg=COLOR_2, relief="flat", cursor="hand2", command=cambiar_modo)
    btn_switch.grid(row=6, column=0)

    # La tecla Enter también manda el formulario
    def al_presionar_enter(evento):
        handle_btn()

    entry_usuario.bind("<Return>", al_presionar_enter)
    entry_contra.bind("<Return>", al_presionar_enter)
