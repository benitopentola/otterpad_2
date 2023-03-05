import tkinter.messagebox as messagebox
import sys

def close_program():
    result = messagebox.askyesno("Cerrar programa", "¿Está seguro de que desea cerrar el programa?")
    if result == True:
        sys.exit()
