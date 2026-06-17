import tkinter as tk
import json
import os
from PIL import Image, ImageTk

folder = os.path.dirname(__file__)

#-------------------------------------------------------------------
#Funciones de json de datos de registro y login (poner las de romu)
#--------------------------------------------------------------------

def mock_login(usuario, contrasena):
    return False, "Falta funcion de romu"

def mock_registrar(usuario, contrasena):
    return False, "Falta funcion de romu"

#---------------------------------------------
#Colores y fuentes
#---------------------------------------------

COLOR_FONDO = "#0A1628"
COLOR_PANEL = "#858585"
COLOR_1 = "#fffc39"
COLOR_1_HOV = "#D6C44CFF"
COLOR_TEXTO = "#F0E6D3"
COLOR_2 = "#FFFFFF"
COLOR_ROJO = "#FF4D6D"
COLOR_VERDE = "#4DFFB4"

FUENTE_TITULO = ("Georgia", 45, "bold")
FUENTE_LABEL = ("Courier New", 10, "bold")
FUENTE_ENTRY = ("Courier New", 11)
FUENTE_BTN = ("Courier New", 11, "bold")
FUENTE_SMALL  = ("Courier New", 10)


#---------------------------------------------
#Pantalla login
#---------------------------------------------

modo = "login"  #variable global para saber si estamos en login o registro
 
def mostrar_login(root, img_fondo, on_success, numero_jugador=1):
 
    global modo
    modo = "login"
 
    #Frame principal
    frame = tk.Frame(root, bg=COLOR_FONDO)
    frame.place(x=0, y=0, width=900, height=600)
 
    # Fondo
    canvas = tk.Canvas(frame, width=900, height=600,
                       highlightthickness=0, bg=COLOR_FONDO)
    canvas.place(x=0, y=0)
    canvas.create_image(0, 0, anchor="nw", image=img_fondo)
 
    #Título
    canvas.create_text(450, 90, text="TOWER DEFENSE",
                       font=FUENTE_TITULO, fill=COLOR_1)
    canvas.create_text(450, 140, text="Defensa y Asalto de Base",
                       font=FUENTE_SMALL, fill=COLOR_2)
 
    #Panel de login
    panel = tk.Frame(frame, bg=COLOR_PANEL, padx=36, pady=28,
                     highlightbackground=COLOR_1, highlightthickness=1)
    canvas.create_window(450, 360, window=panel)
 
    #Título del panel
    lbl_titulo = tk.Label(panel, text=f"LOG IN - PLAYER {numero_jugador}",
                      font=("Courier New", 13, "bold"),
                      bg=COLOR_PANEL, fg=COLOR_1)
    lbl_titulo.grid(row=0, column=0, pady=(0, 18))


    #Usuario
    tk.Label(panel, text="USER", font=FUENTE_LABEL,
             bg=COLOR_PANEL, fg=COLOR_2).grid(row=1, column=0, sticky="w")
    entry_usuario = tk.Entry(panel, font=FUENTE_ENTRY, width=26,
                             bg="#0A1E38", fg=COLOR_TEXTO,
                             insertbackground=COLOR_TEXTO, relief="flat",
                             highlightbackground=COLOR_1, highlightthickness=1)
    entry_usuario.grid(row=2, column=0, pady=(4, 12))
 
    #Contraseña
    tk.Label(panel, text="PASSWORD", font=FUENTE_LABEL,
             bg=COLOR_PANEL, fg=COLOR_2).grid(row=3, column=0, sticky="w")
    entry_contra = tk.Entry(panel, font=FUENTE_ENTRY, width=26,
                            bg="#0A1E38", fg=COLOR_TEXTO,
                            insertbackground=COLOR_TEXTO, relief="flat",
                            highlightbackground=COLOR_1, highlightthickness=1,
                            show="●")
    entry_contra.grid(row=4, column=0, pady=(4, 20))
 
    #Mensaje error o éxito
    lbl_msg = tk.Label(panel, text="", font=FUENTE_SMALL,
                       bg=COLOR_PANEL, fg=COLOR_ROJO, wraplength=260)
    lbl_msg.grid(row=7, column=0, pady=(12, 0))


    #Funciones internas
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
            lbl_titulo.config(text="LOG IN")
            btn_main.config(text="ENTER")
            btn_switch.config(text="Don't have an account? Create one")
 
    def handle_btn():
        global modo
        usuario    = entry_usuario.get().strip()
        contrasena = entry_contra.get().strip()
 
        if not usuario or not contrasena:
            lbl_msg.config(text="Please fill in everything.", fg=COLOR_ROJO)
            return
 
        if modo == "login":
            #cambiar funcion mock login por la de romu
            ok, resultado = mock_login(usuario, contrasena)
            if ok:
                lbl_msg.config(text=f"Welcome, {usuario}!", fg=COLOR_VERDE)
                resultado["usuario"] = usuario
                frame.after(600, lambda: on_success(resultado))
            else:
                lbl_msg.config(text=resultado, fg=COLOR_ROJO)
        else:
            # Reemplazá mock_registrar por la función de Romu cuando esté
            ok, resultado = mock_registrar(usuario, contrasena)
            if ok:
                lbl_msg.config(text="Account created! Please log in.", fg=COLOR_VERDE)
                frame.after(1000, cambiar_modo)
            else:
                lbl_msg.config(text=resultado, fg=COLOR_ROJO)

    #Botón principal
    btn_main = tk.Button(panel, text="ENTER", font=FUENTE_BTN, bg=COLOR_1, fg="#0A1628", relief="flat", cursor="hand2", width=24, pady=7, command=handle_btn)
    btn_main.grid(row=5, column=0, pady=(0, 8))
 
    #Botón cambiar modo
    btn_switch = tk.Button(panel, text="Don't have an account? Create one", font=FUENTE_SMALL, bg=COLOR_PANEL, fg=COLOR_2, relief="flat", cursor="hand2", command=cambiar_modo)
    btn_switch.grid(row=6, column=0)
 
    #Tecla enter para que envie
    root.bind("<Return>", lambda e: handle_btn())



#loop y prueba
if __name__ == "__main__":
    root = tk.Tk()
    root.title("Mundial 2026 — Login")
    root.geometry("900x600")
    root.resizable(False, False)
 
    img_fondo = ImageTk.PhotoImage(Image.open(os.path.join(folder, "menu_bg_night.png")).resize((900, 600)))
 
    def cuando_entra(jugador):
        print("Jugador:", jugador)
 
    mostrar_login(root, img_fondo=img_fondo, on_success=cuando_entra, numero_jugador=1)
    root.mainloop()