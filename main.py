import sys
import os
 
# permite importar los modulos de core/ y ui/ sin problema
sys.path.append(os.path.join(os.path.dirname(__file__), "core"))
sys.path.append(os.path.join(os.path.dirname(__file__), "ui"))
 
import tkinter as tk
 
 
def main():
    root = tk.Tk()
    root.title("Defensa y Asalto de Base")
    root.geometry("900x650")
    root.resizable(False, False)

    #aqui empieza lo de valerio

    root.mainloop()
 
 
if __name__ == "__main__":
    main()