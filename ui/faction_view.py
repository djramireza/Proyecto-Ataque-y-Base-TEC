import tkinter as tk
from constantes import *

# pantalla de seleccion de faccion

#  Uso desde main.py:
#  mostrar_facciones(root, img_fondo, img_madagascar, img_argentina, img_india,
#                   numero_jugador=1, faccion_tomada=None, on_success=...)


def mostrar_facciones(root, img_fondo, img_madagascar, img_argentina, img_india,
                      numero_jugador=1, faccion_tomada=None, on_success=None):

    #faccion_tomada es la facción que ya eligió el otro jugador (no se puede elegir)
    faccion_elegida = {"valor": None}  #usamos dict para poder modificarlo adentro de las funciones

    #Frame principal
    frame = tk.Frame(root, bg=COLOR_FONDO)
    frame.place(x=0, y=0, width=ANCHO, height=ALTO)

    #Fondo
    canvas = tk.Canvas(frame, width=ANCHO, height=ALTO,
                       highlightthickness=0, bg=COLOR_FONDO)
    canvas.place(x=0, y=0)
    canvas.create_image(0, 0, anchor="nw", image=img_fondo)

    #Título
    canvas.create_text(450, 90, text="CHOOSE YOUR FACTION",
                       font=FUENTE_TITULO, fill=COLOR_1)
    canvas.create_text(450, 130, text=f"Player {numero_jugador}",
                       font=FUENTE_SMALL, fill=COLOR_2)

    #Mensaje de error
    lbl_msg = tk.Label(frame, text="", font=FUENTE_SMALL,
                       bg=COLOR_FONDO, fg=COLOR_ROJO)
    lbl_msg.place(x=450, y=530, anchor="center")

    #Tarjetas de facciones
    facciones_info = [
        ("Madagascar", img_madagascar, 175),
        ("Argentina",  img_argentina,  450),
        ("India",      img_india,      725), ]

    botones = {}  #guardamos referencia a cada botón para cambiar su color

    def seleccionar(nombre):
        #Si la facción está tomada no hace nada
        if nombre == faccion_tomada:
            return
        faccion_elegida["valor"] = nombre
        lbl_msg.config(text="")

        #Resaltamos el seleccionado y apagamos los demás
        for n, btn in botones.items():
            if n == nombre:
                btn.config(bg=COLOR_1, fg="#0A1628")
            elif n == faccion_tomada:
                btn.config(bg="#444444", fg="#888888")
            else:
                btn.config(bg=COLOR_FONDO, fg=COLOR_2)

    def confirmar():
        if faccion_elegida["valor"] is None:
            lbl_msg.config(text="Please select a faction first.")
            return
        if on_success:
            on_success(faccion_elegida["valor"])

    #Dibujamos las 3 tarjetas
    for nombre, imagen, x in facciones_info:
        tomada = (nombre == faccion_tomada)

        #Imagen de la facción
        canvas.create_image(x, 280, anchor="center", image=imagen)

        #Nombre de la facción
        color_texto = "#888888" if tomada else COLOR_2
        canvas.create_text(x, 385, text=nombre,
                           font=FUENTE_BTN, fill=color_texto)

        #Texto "TAKEN" si ya fue elegida
        if tomada:
            canvas.create_text(x, 410, text="TAKEN",
                               font=FUENTE_SMALL, fill=COLOR_ROJO)

        #Botón de selección
        color_btn = "#444444" if tomada else COLOR_FONDO
        color_fg  = "#888888" if tomada else COLOR_2
        btn = tk.Button(frame, text="SELECT", font=FUENTE_BTN,
                        bg=color_btn, fg=color_fg, relief="flat",
                        cursor="hand2" if not tomada else "arrow",
                        width=12, pady=5,
                        command=lambda n=nombre: seleccionar(n))
        btn.place(x=x, y=430, anchor="center")
        botones[nombre] = btn

    #Botón confirmar
    btn_confirmar = tk.Button(frame, text="CONFIRM", font=FUENTE_BTN,
                              bg=COLOR_1, fg="#0A1628", relief="flat",
                              cursor="hand2", width=20, pady=8,
                              command=confirmar)
    btn_confirmar.place(x=450, y=490, anchor="center")


#prueba rapidita


if __name__ == "__main__":
    from PIL import Image, ImageTk
    import os
    folder = os.path.dirname(__file__)

    root = tk.Tk()
    root.title("Facciones")
    root.geometry("900x600")
    root.resizable(False, False)

    #imagenes
    img_fondo      = ImageTk.PhotoImage(Image.open(os.path.join(folder, "menu_bg_night.png")).resize((900, 600)))
    img_madagascar = ImageTk.PhotoImage(Image.open(os.path.join(folder, "madagascar_fc.png")).resize((200, 200)))
    img_argentina  = ImageTk.PhotoImage(Image.open(os.path.join(folder, "argentina_fc.png")).resize((200, 200)))
    img_india      = ImageTk.PhotoImage(Image.open(os.path.join(folder, "india_fc.png")).resize((200, 200)))

    def cuando_elige(faccion):
        print("Facción elegida:", faccion)

    #Probá cambiando faccion_tomada="Madagascar" para ver cómo se ve bloqueada
    mostrar_facciones(root, img_fondo, img_madagascar, img_argentina, img_india,
                      numero_jugador=1, faccion_tomada=None, on_success=cuando_elige)

    root.mainloop()