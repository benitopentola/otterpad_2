import tkinter as tk
import webbrowser

def open_webpage():
    if entry.get() == "":
        webbrowser.open("https://www.ilerna.es/")
    else:
        webbrowser.open(entry.get())

root = tk.Tk()
root.title("Navegador web en Python")

entry = tk.Entry(root, width=50)
entry.pack()

button = tk.Button(root, text="Ir", command=open_webpage)
button.pack()

open_webpage()

root.mainloop()
