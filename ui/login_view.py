import tkinter as tk
import json
import os
from PIL import Image, ImageTk

folder = os.path.dirname(__file__)

#-------------------------------------------------------------------
#Funciones de json de datos de registro y login (poner las de romu)
#--------------------------------------------------------------------

def mock_login(usuario, contrasena):
    return

def mock_registrar(usuario, contrasena):
    return

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

class Main_Menu(tk.Frame):

    def __init__(self, master, on_success, img_fondo):
        super().__init__(master, bg=COLOR_FONDO) #Esto es para poder hacer el frame pq sin esto no sirve tkinter
        self.on_success = on_success  # función que se llama cuando el jugador entra
        self.img_fondo  = img_fondo   # imagen que viene desde el main
        self.modo = "login"           # login o registro
        self._construir()

    def _construir(self):

        #Fondo
        canvas = tk.Canvas(self, width=900, height=600,
                           highlightthickness=0, bg=COLOR_FONDO)
        canvas.place(x=0, y=0)

        canvas.create_image(0, 0, anchor="nw", image=self.img_fondo)

        #Titulo
        canvas.create_text(450, 90, text="TOWER DEFENSE",
                        font=FUENTE_TITULO, fill=COLOR_1)
        canvas.create_text(450, 140, text="Defensa y Asalto de Base",
                           font=FUENTE_SMALL, fill=COLOR_2)
        
        #Panel de login
        panel = tk.Frame(self, bg=COLOR_PANEL, padx=36, pady=28,
                         highlightbackground=COLOR_1, highlightthickness=1)
        canvas.create_window(450, 360, window=panel)

        #Titulo
        self.lbl_titulo = tk.Label(panel, text="LOG IN",
                                   font=("Courier New", 13, "bold"),
                                   bg=COLOR_PANEL, fg=COLOR_1)
        self.lbl_titulo.grid(row=0, column=0, pady=(0, 18))

        #Usuario
        tk.Label(panel, text="USER", font=FUENTE_LABEL,
                 bg=COLOR_PANEL, fg=COLOR_2).grid(row=1, column=0, sticky="w")
        self.entry_usuario = tk.Entry(panel, font=FUENTE_ENTRY, width=26,
                                      bg="#0A1E38", fg=COLOR_TEXTO,
                                      insertbackground=COLOR_TEXTO, relief="flat",
                                      highlightbackground=COLOR_1,
                                      highlightthickness=1)
        self.entry_usuario.grid(row=2, column=0, pady=(4, 12))

        #Contraseña
        tk.Label(panel, text="PASSWORD", font=FUENTE_LABEL,
                 bg=COLOR_PANEL, fg=COLOR_2).grid(row=3, column=0, sticky="w")
        self.entry_contra = tk.Entry(panel, font=FUENTE_ENTRY, width=26,
                                     bg="#0A1E38", fg=COLOR_TEXTO,
                                     insertbackground=COLOR_TEXTO, relief="flat",
                                     highlightbackground=COLOR_1,
                                     highlightthickness=1, show="●")
        self.entry_contra.grid(row=4, column=0, pady=(4, 20))

        #Boton principal
        self.btn_main = tk.Button(panel, text="ENTRAR", font=FUENTE_BTN,
                                  bg=COLOR_1, fg="#0A1628", relief="flat",
                                  cursor="hand2", width=24, pady=7,
                                  command=self._handle_btn)
        self.btn_main.grid(row=5, column=0, pady=(0, 8))

        #Cambiar a registro
        self.btn_switch = tk.Button(panel, text="Don't have an account? Create one",
                                    font=FUENTE_SMALL, bg=COLOR_PANEL,
                                    fg=COLOR_2, relief="flat", cursor="hand2",
                                    command=self._cambiar_modo)
        self.btn_switch.grid(row=6, column=0)

        #Mensaje error o exito
        self.lbl_msg = tk.Label(panel, text="", font=FUENTE_SMALL,
                                bg=COLOR_PANEL, fg=COLOR_ROJO, wraplength=260)
        self.lbl_msg.grid(row=7, column=0, pady=(12, 0))

        # Enter también envía el formulario
        self.master.bind("<Return>", lambda e: self._handle_btn())


    def _cambiar_modo(self):
        self.lbl_msg.config(text="")
        if self.modo == "login":
            self.modo = "registro"
            self.lbl_titulo.config(text="CREATE ACCOUNT")
            self.btn_main.config(text="REGISTER")
            self.btn_switch.config(text="Already registered? Login")
        else:
            self.modo = "login"
            self.lbl_titulo.config(text="LOG IN")
            self.btn_main.config(text="ENTER")
            self.btn_switch.config(text="Don't have an account? Create one")

    def _handle_btn(self):
        usuario = self.entry_usuario.get().strip()
        contrasena = self.entry_contra.get().strip()

        if not usuario or not contrasena:
            self.lbl_msg.config(text="Please fill in everything.", fg=COLOR_ROJO)
            return

        if self.modo == "login":
            #cambiar mock_login con la funcion de romu
            ok, resultado = mock_login(usuario, contrasena)
            if ok:
                self.lbl_msg.config(text=f"Welcome!, {usuario}!", fg=COLOR_VERDE)
                resultado["usuario"] = usuario
                self.after(600, lambda: self.on_success(resultado))
            else:
                self.lbl_msg.config(text=resultado, fg=COLOR_ROJO)
        else:
            #cambiar mock_registrar con la funcion de romu
            ok, resultado = mock_registrar(usuario, contrasena)
            if ok:
                self.lbl_msg.config(text="Account succesfully created! Please log in", fg=COLOR_VERDE)
                self.after(1000, self._cambiar_modo)
            else:
                self.lbl_msg.config(text=resultado, fg=COLOR_ROJO)



#loop y prueba
if __name__ == "__main__":
    root = tk.Tk()
    root.title("Mundial 2026 — Login")
    root.geometry("900x600")
    root.resizable(False, False)
 
    # Acá cargás TODAS las imágenes, el root ya existe así que no explota
    img_fondo = ImageTk.PhotoImage(Image.open(os.path.join(folder, "menu_bg_night.png")).resize((900, 600)))
 
    def cuando_entra(jugador):
        print("Jugador:", jugador)
 
    # Las imágenes se las pasás a la clase como parámetro
    vista = Main_Menu(root, on_success=cuando_entra, img_fondo=img_fondo)
    vista.pack(fill="both", expand=True)
    root.mainloop()